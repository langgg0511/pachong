import requests
res = requests.get('http://lol.qq.com/web201310/info-heros.shtml')
print(res)
res.encoding = 'utf-8'






