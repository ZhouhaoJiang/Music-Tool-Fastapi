import requests
from requests_html import HTMLSession


url = "https://music.163.com/api/playlist/detail?id=19723756"

response = requests.get(url)
data = response.json()
print(data)
