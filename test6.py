import requests
from bs4 import BeautifulSoup
import json
import pandas

first_url = 'http://www.ximalaya.com/dq'
headers = {'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
commond = []
def request_content(url):
    request = requests.get(url, headers=headers)
    request.encoding = 'utf-8'
    text = request.text
    return text

def get_url(url):
    soup = BeautifulSoup(request_content(url), 'html.parser')
    url_list =soup.find_all(class_='discoverAlbum_title')
    new_url = []
    for list_href in url_list:
        new_url.append(list_href['href'])
    return new_url

def get_soup(url):
    request_content(url)
    soup = BeautifulSoup(request_content(url), 'html.parser')
    return soup

def get_parse(url):
    soup = get_soup(url)
    name = soup.select('div .detailContent_title')[0].text
    print('正在获取《%s》音频' % name)
    sound_ids = soup.select('.personal_body')[0]['sound_ids']
    sound_id = str(sound_ids).split(',')

    for id in sound_id:
        sound_item = soup.find('li', attrs={'sound_id': id}).text.split()
        # print(sound_item)
        commond.append((sound_item[0:-2], get_sound_mp4(id), sound_item[-2]))
        pandas.set_option('max_colwidth', 200)
    data1 = pandas.DataFrame(commond, columns=['name', 'time', 'url'])
    data1.to_csv(r'D:\pythontest\pachong\xmly.csv', header=False, index=False, encoding='utf_8_sig')
    next_html = get_next_url(url)
    while next_html:
        get_parse(next_html)

def get_sound_mp4(id):  #获取音频ID
    sound_mp4_url = 'http://www.ximalaya.com/tracks/{}.json'.format(str(id))
    sound_mp4 = request_content(sound_mp4_url)
    dict = json.loads(sound_mp4)
    return dict.get('play_path')

def get_next_url(url):  #获得下一页的URL
    soup = get_soup(url)
    try:
        next_url_href = soup.find('a', attrs={'rel': 'next'})['href']#加一个异常捕获！！！！！！！！！！
    except TypeError:
        return
    if next_url_href:
        next_html = 'http://www.ximalaya.com/{}'.format(next_url_href)
        return next_html
    else:
         return None


def main(url):
    new_url = get_url(url)
    for list in new_url:
        get_parse(list)

if __name__ == '__main__':
    main(first_url)