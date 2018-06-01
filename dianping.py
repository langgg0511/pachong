from selenium import webdriver
import time
from xpathtest.proxy import ProxyList
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}
proxys = ProxyList()
ip = proxys.get_proxy()
dacp = dict(DesiredCapabilities.PHANTOMJS)
dacp["phantomjs.page.settings.proxy"] = ip
dacp["phantomjs.page.settings.loadImages"] = False
dacp["phantomjs.page.settings.userAgent"] = header
proxy = webdriver.Proxy()
proxy.proxy_type = ProxyType.MANUAL
proxy.http_proxy = ip
driver = webdriver.PhantomJS(
    executable_path=r"C:\Users\wu\AppData\Roaming\Python\Python36\site-packages\phantomjs-2.1.1-windows\bin\phantomjs.exe")
url = 'http://www.dianping.com/shaoguan/ch10'
driver.get(url)
time.sleep(3)
pageSource = driver.page_source
print(pageSource)