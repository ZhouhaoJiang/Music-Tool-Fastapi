import csv
import pymysql
import untils
import hashlib

mysql_host = untils.mysql_host
mysql_port = untils.mysql_port
mysql_user = untils.mysql_user
mysql_password = untils.mysql_password
mysql_database = untils.mysql_database

# 创建连接
con = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, port=mysql_port, charset="utf8",
                      database=mysql_database)

# md5加密
def md5(password):
    md5 = hashlib.md5()
    md5.update(password.encode("utf-8"))
    return md5.hexdigest()


def create_user(username, password):
    password = md5(password)

    try:
        with con.cursor() as cur:
            # 判断用户是否存在
            if cur.execute("SELECT * FROM User WHERE username = %s", (username,)):
                return {"status": 400, "msg": "User Already Exists"}

            # 创建用户
            sql = """
                INSERT INTO User (username, password) VALUES (%s, %s);
            """
            cur.execute(sql, (username, password))
            con.commit()

            return {"status": 200, "msg": "Success Create User"}
    except Exception as e:
        con.rollback()
        print(e)
        return {"status": 400, "msg": "Failed Create User"}


def login_user(username, password):
    password = md5(password)
    try:
        with con.cursor() as cur:
            # 判断用户是否存在
            if cur.execute("SELECT * FROM User WHERE username = %s", (username,)):
                # 判断密码是否正确
                if cur.execute("SELECT * FROM User WHERE username = %s AND password = %s", (username, password)):
                    return {"status": 200, "msg": "Success Login"}
                else:
                    return {"status": 400, "msg": "Password Error"}
            else:
                return {"status": 400, "msg": "User Not Exists"}
    except Exception as e:
        print(e)
        return {"status": 400, "msg": "Failed Login"}

