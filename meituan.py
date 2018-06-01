from selenium import webdriver
import time
from lxml import etree
import pandas
from xpathtest.headers import get_header
import numpy
# from xpathtest.proxy import ProxyList

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class MeiTuan:
    def __init__(self):
        self.url = 'http://sg.meituan.com/meishi/'
        self.dict_url = 'http://sg.meituan.com/meishi/api/poi/getPoiList?uuid=db094399-1612-437a-bab7-c470070d360c&platform=1&partner=126&originUrl=http://sg.meituan.com/meishi/pn1/&riskLevel=1&optimusCode=1&cityName=韶关&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=1&userId=0'
    # def get_proxy(self):
    #     proxy = ProxyList()
    #     return proxy.get_proxy()
    def get_headers(self):
        return get_header()

    def get_meituan(self):
        # content = urlrequest.urlopen(self.url).read()
        headers = self.get_headers()
        # ip = self.get_proxy()
        # proxy = ProxyList()
        # ip = proxy.get_proxy()
        head = headers['User-Agent']
        # print(headers)
        # print(head)
        # print(ip)

        dacp = dict(DesiredCapabilities.PHANTOMJS)
        dacp["phantomjs.page.settings.userAgent"] = head
        driver = webdriver.PhantomJS(
            executable_path=r"C:\Users\wu\AppData\Roaming\Python\Python36\site-packages\phantomjs-2.1.1-windows\bin\phantomjs.exe")
        n = 0
        foot_frame = pandas.DataFrame(index=range(0, 436), columns=['name', 'avgScore', 'allComment', 'address', 'avgPrice', 'href'])
        for m in range(1, 15):
            url = self.url + 'pn' + str(m) + '/'
            # print(url)
            driver.get(url)
            time.sleep(3)
            pageSource = driver.page_source
            # print(pageSource)
            lxml = etree.HTML(pageSource)
            foot_list = lxml.xpath('//ul[@class="list-ul"]//li[@class="clear btm"]|//ul[@class="list-ul"]//li[@class="clear"]')
            # print(foot_list)
            # print(len(foot_list))
            for i in range(1, len(foot_list)):
                name = lxml.xpath('//ul[@class="list-ul"]/li[{0}]/div[@class="info"]/a/h4/text()'.format(i+1))
                # print(name)
                href = lxml.xpath('//ul[@class="list-ul"]/li[{0}]/div[@class="info"]/a/@href'.format(i+1))
                avgScore = lxml.xpath('//ul[@class="list-ul"]/li[{0}]/div[@class="info"]/a/div[@class="source clear"]/p/text()'.format(i+1))
                allComment = lxml.xpath('//ul[@class="list-ul"]/li[{0}]/div[@class="info"]/a/div[@class="source clear"]/p/span/text()'.format(i+1))
                address = lxml.xpath('//ul[@class="list-ul"]/li[{0}]/div[@class="info"]/a/p[@class="desc"]/text()'.format(i+1))
                avgPrice = lxml.xpath('//ul[@class="list-ul"]/li[{0}]/div[@class="info"]/a/p[@class="desc"]/span/text()'.format(i+1))
                foot_frame['name'][n] = name[0]
                foot_frame['href'][n] = href[0]
                foot_frame['avgScore'][n] = avgScore[0]
                foot_frame['allComment'][n] = allComment[0]
                foot_frame['address'][n] = address[0]
                foot_frame['avgPrice'][n] = avgPrice[-1]
                n = n+1
            print("第" + str(m) + "页爬取完成")
            # return foot_frame
        driver.close()
        return foot_frame
        # driver.close()
            # lxml = etree.HTML(pageSource)
            # yanzhenma = lxml.xpath('//img[@id="yodaImgCode"]/@src')
            # content = requests.get(self.url).text
            # Image.open(yanzhenma)

            # print(yanzhenma)

    def get_meituancsv(frame):
        frame.to_csv('D:/pythontest/xpathtest/meituanframe.csv', encoding='gbk', index=False)

if __name__ == '__main__':
    meituan = MeiTuan()
    frame = meituan.get_meituan()
    meituan.get_meituancsv(frame)
