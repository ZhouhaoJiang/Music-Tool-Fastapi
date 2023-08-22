# docker运行
```bash
# 拉取项目代码
git clone https://git.bitnet.fun:5004/Jiang/thief_music_api.git

# 进入项目目录
cd thief_music_api

# 构建docker镜像
docker build -t thief_music .

# 从运行docker容器
docker run -d --name thief_music -p 7788:7788 thief_music
```