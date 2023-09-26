import fastapi
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from datetime import timedelta
import requests
import uvicorn
from fastapi import Depends
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_login import LoginManager
from server.user_server import *
from server.rank_data import *
from server.music_server import *
from fake_useragent import UserAgent

env = os.environ
app = FastAPI()

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，可以根据需求进行配置
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有请求方法
    allow_headers=["*"],  # 允许所有请求头
)

SECRET = os.urandom(24).hex()
manager = LoginManager(SECRET, token_url='/auth/token', use_cookie=False)

try:
    # mysql数据配置
    con = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, port=mysql_port,
                          charset="utf8", database=mysql_database)
    # cursor = con.cursor()
except Exception as e:
    print(e)
    print("数据库连接失败")


@manager.user_loader()
def load_user(username: int):
    """
    获取用户信息
    :param username:
    :return:
    """
    try:
        with con.cursor() as cursor:
            cursor.execute("SELECT * FROM User WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user:
                user_dict = dict(username=user[1], password=user[3])
                return user_dict
            else:
                return None
    except Exception as e:
        print(e)
        return None


# @app.get('/auth/cookie')
# def auth(response: Response, user=Depends(manager)):
#     """
#     通过cookie验证用户
#     :param response:
#     :param user:
#     :return:
#     """
#     # 查询用户信息
#     cursor.execute("SELECT * FROM User WHERE email = %s", (user['sub'],))
#     user = cursor.fetchone()
#     # 生成token
#     token = manager.create_access_token(
#         data=dict(sub=user[2])
#     )
#     manager.set_cookie(response, token)
#     return response


@app.post('/auth/get_token')
def get_token(data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = md5(data.password)

    user = load_user(username)  # we are using the same function to retrieve the user
    if not user:
        raise InvalidCredentialsException  # you can also use your own HTTPException
    elif password != user['password']:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=username),
        expires=timedelta(hours=12)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


# 验证Token
@app.get('/token/verify_user')
def get_current_user(current_user=Depends(manager.get_current_user)):
    if current_user:
        return {"status": 200, "success": True, "message": "Validated successfully"}
    else:
        return {"status": 400, "success": False, "message": "Invalid token"}


# @app.get('/protected')
# def protected_route(user=Depends(manager)):
#     return "验证通过"


# 注册
@app.post("/user/register")
async def user_register(
        username: str = fastapi.Query(..., description="用户名"),
        password: str = fastapi.Query(..., description="密码"),
        email: str = fastapi.Query(None, description="邮箱")):
    """
    注册
    :param username:
    :param password:
    :param email:
    :return:
    """
    result = create_user(username, password)
    if result["status"] == 200:
        # 用户创建成功，获取 token 并返回成功响应
        token_info = get_token(OAuth2PasswordRequestForm(username=username, password=password))
        return {"success": True, "message": "注册成功", "token": token_info}
    elif result["status"] == 400 and result["msg"] == "User Already Exists":
        # 用户已存在，返回相应的错误响应
        return {"success": False, "message": "用户已存在"}
    else:
        # 创建用户失败，返回相应的错误响应
        return {"success": False, "message": "创建用户失败"}


# 登陆
@app.post("/user/login")
async def user_login(
        username: str = fastapi.Query(..., description="用户名"),
        password: str = fastapi.Query(..., description="密码")):
    """
    登陆并获取Token
    :param username:
    :param password:
    :return:
    """
    # 请求auth/token接口获取token
    login_info = login_user(username, password)
    if login_info['status'] == 200:
        token_info = get_token(OAuth2PasswordRequestForm(username=username, password=password))
        return {"success": True, "message": "login success", "token": token_info}
    else:
        return {"success": False, "message": login_info['msg']}


# 榜单获取
@app.get("/get_rank")
async def get_rank(
        rank_id: str = fastapi.Query(..., description="榜单类型")):
    # current_user=Depends(manager.get_current_user)
    """
    :param rank_id:
    19723756 云音乐飙升榜
    3779629 云音乐新歌榜
    3778678 云音乐热歌榜
    2884035 云音乐原创榜
    :return:
    """
    ua = UserAgent()
    headers = {
        "Referer": "https://music.163.com/",
        "User-Agent": ua.random
    }
    url = f"https://music.163.com/api/playlist/detail?id={rank_id}"

    # 尝试从网络获取最新数据
    response = requests.get(url, headers=headers)
    json_data = response.json()

    if json_data['code'] != 200:
        return {"message": "Failed to fetch data from Netease Cloud API", "data": read_cache(rank_id)}
    else:
        # 检测是否含有带rank_id的缓存文件
        cached_data = read_cache(rank_id)

        if cached_data:
            # 如果缓存数据存在，比较缓存数据与新数据的内容，如果不同则更新缓存
            if cached_data != response.json():
                write_cache(rank_id, response.json())
            return {"message": "local json data", "data": cached_data}
        else:
            # 如果缓存数据不存在，则将新数据写入缓存
            write_cache(rank_id, response.json())
            return {"message": "Request Netease Cloud And Local Cache JSON Success", "data": response.json()}


@app.get("/search_song_by_name")
async def search_song_by_name(
        name: str = fastapi.Query(..., description="歌曲名称"),
        # current_user=Depends(manager.get_current_user)
):
    payload = {
        "input": name,
        "filter": "name",
        "type": "netease",  # netease, tencent, kugou, xiami, baidu
        "page": 1
    }

    # url = "https://sunpma.com/other/musicss/"
    url = "https://music.ghser.com/"
    # Headers for the POST request
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "sec-ch-ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest"
    }
    # 将所有 headers 的值用 'utf-8' 进行编码
    # headers = {key: value.encode('utf-8') for key, value in headers.items()}

    # Making the POST request
    response = requests.post(url, data=payload, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the response JSON data
        data = response.json()

        return {"message": "success", "data": data}
    else:
        print(f"Failed to get data. Status code: {response.status_code}")
        return {"message": "failed", "data": []}


# 根据歌曲id搜索歌曲
@app.get("/search_song_by_id")
async def search_song_by_id(
        music_id: str = fastapi.Query(..., description="歌曲id"),
        # current_user=Depends(manager.get_current_user)
):
    payload = {
        "input": music_id,
        "filter": "id",
        "type": "netease",  # netease, tencent, kugou, xiami, baidu
        "page": 1
    }
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "sec-ch-ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest"
    }

    # url = "https://sunpma.com/other/musicss/"
    url = "https://music.ghser.com/"

    # Making the POST request
    response = requests.post(url, data=payload, headers=headers, timeout=10)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the response JSON data
        data = response.json()
        print(data)
        try:
            save_search_music(data)
        except Exception as e:
            print(e)
        return {"message": "success", "data": data}
    else:
        print(f"Failed to get data. Status code: {response.status_code}")
        return {"message": "failed", "data": []}


if __name__ == '__main__':
    host = env.get("HOST") if env.get("HOST") is not None else "0.0.0.0"
    port = int(env.get("PORT")) if env.get("PORT") is not None else 8000
    uvicorn.run(app='api:app', host=host, port=port, reload=True)
