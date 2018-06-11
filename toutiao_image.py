# -*- coding:utf-8 -*-
# 2018-06-07

import requests
from urllib.parse import urlencode
from urllib.request import urlopen
import urllib
from selenium import webdriver
import os
import time
import re

headers1 = {
    'Accept': 'application / json, text / javascript',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh - CN, zh;q = 0.8, zh - TW;q = 0.7, zh - HK;q = 0.5, en - US;q = 0.3, en;q = 0.2',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'www.toutiao.com',
    'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'X - Requested - With': 'XMLHttpRequest'
}
headers2 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh - CN, zh;q = 0.8, zh - TW;q = 0.7, zh - HK;q = 0.5, en - US;q = 0.3, en;q = 0.2',
    'Connection': 'keep-alive',
    'Host': 'www.toutiao.com',
    'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
}


def get_proxies():
    proxy_url = "http://127.0.0.1:5555/random"
    try:
        response = requests.get(proxy_url)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None


def get_json(offset, keyword):
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': '3',
        'from': 'gallery'
    }
    # proxy = get_proxies()
    # if proxy:
    #     proxies = {
    #         'http': 'http://' + proxy,
    #         'https': 'https://' + proxy
    #     }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(params)

    try:
        response = requests.get(url, headers=headers1)
        time.sleep(3)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        print('连接出错，从新访问')
        get_json(offset)


def get_parse(jsons):
    if jsons['data']:
        for item in jsons['data']:
            url = item['share_url']
            title = item['title']
            yield {
                'title': title,
                'url': url
            }


def get_image_url(url):
    import json
    # 添加代理
    # proxy = get_proxies()
    # if proxy:
    # proxies = {
    #     'http': 'http://' + proxy,
    #     'https': 'https://' + proxy
    # }
    # response = requests.get(url, headers=headers2, proxies=proxies)
    # 用无头浏览器打开网页
    driver = webdriver.PhantomJS(
        executable_path=r"C:\Users\wu\AppData\Roaming\Python\Python36\site-packages\phantomjs-2.1.1-windows\bin\phantomjs.exe")
    driver.get(url)
    time.sleep(1)
    response = driver.page_source
    driver.close()
    # 用正则去除图片地址所在位置
    lis = re.findall('parse\("(.*.)"\)', response)
    # 去除lis中的转义符‘\’
    lis1 = re.sub(r'\\', '', lis[0])
    data = json.loads(lis1)
    # 图片数量
    image_count = data['count']
    # 图片地址
    image_list = []
    for i in data['sub_images']:
        image_list.append(i['url'])
    return image_count, image_list


def load_image(title, url_list):
    toutiao_path = r'D:\spider_image\toutiao' + '\\' + title
    name = 0
    if not os.path.exists(toutiao_path):
        os.makedirs(toutiao_path)
    for image_url in url_list:
        try:
            name += 1
            image = urlopen(image_url).read()
            image_name = toutiao_path + '\\' + title + str(name) + '.jpg'
            with open(image_name, 'wb') as f:
                f.write(image)
        except urllib.eerror.HTTPError:
            return
    print(str(title) + "已下载" + str(name) + "张")
    return


if __name__ == '__main__':
    # 要下载图片的关键词,页数
    # 一页有19个图集
    keyword = '小姐姐'
    page_first = 0
    page_end = 3
    for page in range(page_first, page_end):
        json = get_json(page * 20, keyword)
        # url = get_parse(json)
        for item in get_parse(json):
            # print(item)
            # print(item.get('url'))
            title = item['title']
            image_count, image_url_list = get_image_url(item['url'])
            print("开始下载" + str(title) + "  共" + str(image_count) + "张")
            load_image(title, image_url_list)
        print("全部下载完成")
