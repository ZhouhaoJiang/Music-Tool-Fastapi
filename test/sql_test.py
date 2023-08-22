# 导入pymysql
import pymysql
import untils

mysql_host = untils.mysql_host
mysql_port = untils.mysql_port
mysql_user = untils.mysql_user
mysql_password = untils.mysql_password
mysql_database = untils.mysql_database

# 创建连接
con = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password,port=mysql_port, charset="utf8", database=mysql_database)

# 创建游标对象
cursor = con.cursor()

email = "1264204425@qq.com"
# 编写创建表的sql
cursor.execute("SELECT * FROM User WHERE email = %s", (email,))
user = cursor.fetchone()
print(user)


