# 导入pymysql
import pymysql
import config

mysql_host = config.mysql_host
mysql_port = config.mysql_port
mysql_user = config.mysql_user
mysql_password = config.mysql_password

# 创建连接
con = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password,port=mysql_port, charset="utf8")

# 创建游标对象
cur = con.cursor()

# 编写创建表的sql
sql = """
    create database music_sql;
"""

try:
    # 执行创建表的sql
    cur.execute(sql)
    print("创建数据库成功")
    # 关闭游标连接
    cur.close()
    # 关闭数据库连接
    con.close()
except Exception as e:
    print(e)
    print("创建表失败")

