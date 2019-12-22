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
        Item = '世界政區索引'
        google_url = str(self.url)+urllib.parse.quote(Item)
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
    soupIter = crawler.search('1')
    for soup in soupIter:
        tableL = soup.find_all('table')
        for i in range(2,27):
            table = tableL[i]
            trL = table.find_all('tr')
            for j in range(1,len(trL)):
                tr = trL[j]
                tdL = tr.find_all('td')
                country_name = tdL[0].get_text()
                ISO_code = tdL[3].get_text()
                push.insertCountry(country_name,ISO_code)
    push.close()

