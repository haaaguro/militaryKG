#coding=utf-8
import re
import requests
import urllib.request
from bs4 import BeautifulSoup
from CrawlerS import item
from CrawlerS import Connect
from zhconv import convert

class webCrawlerWikiBaike(object):
    def __init__(self, url = 'https://zh.wikipedia.org/wiki/'):
        super(webCrawlerWikiBaike, self).__init__()
        self.url = url
    def search(self, searchItem):
        proxies = {"http": "220.168.237.187:8888","https": "https://127.0.0.1:1080","http": "http://127.0.0.1:1080"}
        headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
        searchItem = '战争列表_(' + searchItem
        google_url = str(self.url)+urllib.parse.quote(searchItem)
        try:
            proxy_handler = urllib.request.ProxyHandler(proxies)  # 设置对应的代理服务器信息
            opener = urllib.request.build_opener(proxy_handler, urllib.request.HTTPHandler)  # 创建一个自定义的opener对象
            urllib.request.install_opener(opener)  # 创建全局默认的opener对象
            req = urllib.request.Request(google_url, headers=headers)
            response = urllib.request.urlopen(req)
            content = response.read().decode("utf-8")
            content = convert(str(content),'zh-hans')
            soupIter = BeautifulSoup(content, 'lxml')
            yield soupIter
        except:
            return '404'
if __name__ == '__main__':
    push = Connect.Connect()
    crawler = webCrawlerWikiBaike()
    timeSet = ['1800年-1899年)','1900年-1944年)','1949年-1985年)','1990年-2002年)','2003年以后)']
    for i in range(0,len(timeSet)):
        searchItem = timeSet[i]
        soupIter = crawler.search(searchItem)
        if soupIter == '404':
            continue
        else:
            for soup in soupIter:
                tableL = soup.find_all('table')
                for n in range(0,len(tableL)):
                    table = tableL[n]
                    trL = table.find_all('tr')
                    for j in range(2,len(trL)):
                        tdL = trL[j].find_all('td')
                        warName = tdL[2].get_text()
                        country1 = tdL[3].find_all('a')
                        countryL=[]
                        if len(country1)>0:
                            for k in range(0,len(country1)):
                                country=country1[k].get_text()
                                if country is not None:
                                    countryL.append(country)
                            if len(tdL)>3:
                                country2 = tdL[4].find_all('a')
                                for m in range(0,len(country2)):
                                    country=country2[m].get_text()
                                    if country is not None:
                                        countryL.append(country)
                        push.insertWarC(warName,countryL)   

    push.close()

