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
# PlaylistSong是歌单的歌曲表关联歌单表和歌曲表
sql = """
CREATE TABLE PlaylistSong (
    id INT AUTO_INCREMENT PRIMARY KEY,
    playlist_id INT NOT NULL,
    songid INT NOT NULL,
    FOREIGN KEY (playlist_id) REFERENCES UserPlayList(playlist_id),
    FOREIGN KEY (songid) REFERENCES Music(songid)
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
