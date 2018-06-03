# -*- coding: utf-8 -*-
#爬取LOL英雄皮肤
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas
import urllib.request as urlrequest
import os
import urllib


def get_herodict():
    url = 'http://lol.qq.com/biz/hero/champion.js'
    content = urlrequest.urlopen(url).read()
    str1 = r'champion={"keys":'
    str2 = r',"data":{"Aatrox":'
    champion = str(content).split(str1)[1].split(str2)[0]
    herodict0 = eval(champion)
    herodict = dict((k, v)for v, k in herodict0.items())
    return herodict

def get_heroframe():
    herodict = get_herodict()
    url_Allhero = 'http://lol.qq.com/web201310/info-heros.shtml#Navi'
    # 使用无头浏览器PhantomJS打开网站，解决javascript动态加载的问题
    driver = webdriver.PhantomJS(
        executable_path=r"C:\Users\wu\AppData\Roaming\Python\Python36\site-packages\phantomjs-2.1.1-windows\bin\phantomjs.exe")
    driver.get(url_Allhero)
    time.sleep(1)

    pageSource = driver.page_source
    driver.close()
    bsObj = BeautifulSoup(pageSource, "lxml")
    herolist = bsObj.findAll('ul', {'class': 'imgtextlist'})
    for hero in herolist:
        n = len(hero)
        m = 0
        heroframe = pandas.DataFrame(index=range(0, n),
                                     columns=['herolink', 'heroickname', 'heroname', 'Englishname', 'heroid'])
        heroinflist = hero.findAll('a')
        for heroinf in heroinflist:
            herolink = heroinf['href']
            heroickname = heroinf['title'].split(' ')[0].strip()
            heroname = heroinf['title'].split(' ')[1].strip()
            heroframe['herolink'][m] = herolink
            heroframe['heroickname'][m] = heroickname
            heroframe['heroname'][m] = heroname
            heroframe['Englishname'][m] = heroframe['herolink'][m][21:]
            heroframe['heroid'][m] = herodict[heroframe['Englishname'][m]]
            m = m + 1
        return heroframe

def get_heroid(heroframe):
    heroid = heroframe['heroid']
    return heroid

def get_herocsv(heroframe):

    heroframe.to_csv('D:/lol/heroframe.csv', encoding='gbk', index=False)

def get_image(heroid, herofram):
    line = herofram[herofram.heroid == heroid].index.tolist()
    #找到所有英雄dataframe所在行
    nickname = herofram['heroickname'][line].values
    name = herofram['heroname'][line].values
    nickname_name = str((nickname + ' ' + name)[0][:])
    filehero = r'D:\lol'+'\\' + nickname_name
    zeor = '00'
    if not os.path.exists(filehero):
        os.makedirs(filehero)
    print("开始下载" + nickname_name + "皮肤")
    for k in range(21):
        url = 'http://ossweb-' \
              'img.qq.com/images/lol/web201310/skin/big' +\
              str(heroid) + zeor + str(k) +'.jpg'

        try:
            image = urlrequest.urlopen(url).read()
            imagename = filehero + '\\' + zeor + str(k) +'.jpg'
            with open(imagename, 'wb') as f:
                f.write(image)
            # urllib.request.urlretrieve(url, filehero)
        except urllib.error.HTTPError:
            print(nickname_name + "爬取完成！")
            print("一共" + str(k) + "张")
            return

    print(nickname + '下载完成')


if __name__ == '__main__':
    heroframe = get_heroframe()
    heroid = get_heroid(heroframe)
    # get_herocsv(heroframe)
    for id_hero in heroid:
        get_image(id_hero, heroframe)
    # get_image(heroid[0], heroframe)
