import requests

# URL for the POST request
url = "https://sunpma.com/other/musicss/"

# Payload data for the POST request
payload = {
    "input": "25906124",
    "filter": "id",
    "type": "netease",
    "page": 1
}

# Headers for the POST request
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://sunpma.com",
    "Referer": f"https://sunpma.com/other/musicss/?id={payload['input']}&type=netease",
    "Sec-Ch-Ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"macOS\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

# Making the POST request
response = requests.post(url, data=payload, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the response JSON data
    data = response.json()
    print(data)
else:
    print(f"Failed to get data. Status code: {response.status_code}")
