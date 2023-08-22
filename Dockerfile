FROM python:3.10.11-slim-buster
WORKDIR /app
COPY . .
RUN pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple/
RUN pip3 install -r requirements.txt
EXPOSE 7788
CMD ["python3", "api.py"]