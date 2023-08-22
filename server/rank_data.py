import datetime
import json
import os


def get_cache_filename(rank_id):
    # 生成缓存文件名，以rank_id命名
    # date_str = datetime.datetime.now().strftime("%Y%m%d")
    return f"{rank_id}.json"


def read_cache(rank_id):
    # 从缓存文件中读取数据
    cache_filename = get_cache_filename(rank_id)
    if os.path.exists(f"data/{cache_filename}"):
        with open(f"data/{cache_filename}", "r", encoding="utf8") as file:
            return json.load(file)
    return None


def write_cache(rank_id, data):
    # 将数据写入缓存文件
    cache_filename = get_cache_filename(rank_id)
    # 创建文件
    if not os.path.exists("data"):
        os.mkdir("data")

    with open(f"data/{cache_filename}", "w", encoding="utf8") as file:
        json.dump(data, file)
