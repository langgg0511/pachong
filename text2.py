import requests
from bs4 import BeautifulSoup
import json
import re
from pachong import text1

Url = 'http://news.sina.com.cn/china/xlxw/2017-11-04/doc-ifynnnsc5806686.shtml'

commentUrl = 'http://comment5.news.sina.com.cn/page/info?\
version=1&format=js&channel=gn&newsid=comos-{}&\
group=&compress=0&ie=utf-8&oe=utf-8&\
page=1&page_size=20&jsvar='

request = requests.get(Url)
request.encoding = 'utf-8'
res = BeautifulSoup(request.text, 'html.parser')
wenzhang = res.select('#artibody p')
def get_times_newsource(newurl):
    result = {}
    m = re.search('doc-i(.*).shtml', newurl)
    newsid = m.group(1)
    comments = requests.get(commentUrl.format(newsid))
    re1 = re.findall('var.*.={', comments.text)[0][:-1]
    request = requests.get(newurl)
    request.encoding = 'utf-8'
    res = BeautifulSoup(request.text, 'html.parser')
    artibodyTitle = res.select('#artibodyTitle')[0].text
    newstime = res.select('#navtimeSource')[0].text.split()[0]  # 获取新闻时间
    newssource = res.select('#navtimeSource')[0].text.split()[1]  # 获取新闻来源
    newshtml = res.select('#navtimeSource span a')[0]['href']  # 获取新闻来源链接
    newseditor = res.select('.article-editor')[0].text.strip('责任编辑：')
    #--------------------------------------------------------------------------------------
    #获取内文
    article = '\n'.join([p.text.strip() for p in res.select('#artibody p')[:-1]])
    #--------------------------------------------------------------------------------
    #获取新闻评论总数
    js = json.loads(comments.text.strip(re1))['result']['count']['total']
    result['newstime'] = newstime
    result['newssource'] = newssource
    result['newshtml'] = newshtml
    result['newseditor'] = newseditor
    result['commentcount'] = js
    result['article'] = article
    result['artibodyTitle'] = artibodyTitle
    return result
timesource = get_times_newsource(Url)
print('新闻日期：' + timesource['newstime'])
print('新闻来源:' + timesource['newssource'] + '\n' +timesource['newshtml'])
print('内文：' + str(timesource['article']))
print('责任编辑：' + timesource['newseditor'])
print('评论总数：' + str(timesource['commentcount']))
print('\n')
