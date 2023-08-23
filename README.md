# docker运行
```bash
# 拉取项目代码
git clone https://github.com/1264204425/Music-Tool-Fastapi.git

# 进入项目目录
cd Music-Tool-Fastapi

# 构建docker镜像
docker build -t Music-Tool-Fastapi .

# 从运行docker容器
docker run -d --name thief_music -p 7788:7788 Music-Tool-Fastapi
```