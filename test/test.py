import requests

url = "https://sunpma.com/other/musicss/?name=%E5%96%9C%E6%AC%A2%E4%BD%A0&type=netease"

# 发送 GET 请求
response = requests.get(url)

# 检查请求是否成功（状态码为 200）
if response.status_code == 200:
    # 获取响应内容
    data = response.json()
    print(data)
else:
    print(f"请求失败。状态码：{response.status_code}")
