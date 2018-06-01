# -*- coding: utf-8 -*-
import requests
from lxml import etree
import time
import re
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}

def get_movie_id(page):
    url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=热门&sort=recommend&page_limit=20&page_start={}'
    for pages in range(0, page):
        url = url.format(pages*20)
        request = requests.get(url, headers=headers)
        request.encoding = 'utf-8'
        json_ = json.loads(request.text)
        movie_id = []
        for i in range(0, 20):
            print(json_['subjects'][i]['other_name'])
        # print(movie_id)



if __name__ == '__main__':
    get_movie_id(1)