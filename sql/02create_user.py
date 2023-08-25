# 导入pymysql
import pymysql
import config

mysql_host = config.mysql_host
mysql_port = config.mysql_port
mysql_user = config.mysql_user
mysql_password = config.mysql_password
mysql_database = config.mysql_database

# 创建连接
con = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password,port=mysql_port, charset="utf8", database=mysql_database)

# 创建游标对象
cur = con.cursor()

# 编写创建表的sql
sql = """
    CREATE TABLE User (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NULL,
    password VARCHAR(255) NOT NULL,
    date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

try:
    # 执行创建表的sql
    cur.execute(sql)
    print("创建成功")
    # 关闭游标连接
    cur.close()
    # 关闭数据库连接
    con.close()
except Exception as e:
    print(e)
    print("创建表失败")

