import requests
url = "http://61.142.33.204"
headers = {'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
request = requests.get(url, headers=headers)
print(request)