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
    iList = push.fullDb()
    for i in range(4240,len(iList)):
         print(i)
         searchItem = iList[i]
         crawler = webCrawlerWikiBaike()
         soupIter = crawler.search(searchItem[0])
         if soupIter == '404':
             continue
         else:
             for soup in soupIter:
                pattern = 1
                textlist = soup.find('div',class_="mw-parser-output")
                table1 = textlist.find('table',class_="infobox vcard")
                trL = None
                label = None
                if table1 is not None:
                    trL = table1.find_all('tr')
                    pattern = 1
                else:
                    table2 = textlist.find('table',class_="infobox")
                    if table2 is not None:
                        trL = table2.find_all('tr')
                        pattern = 0
                if trL is not None:
                    for i in range(0,len(trL)):
                        content=''
                        if pattern==1:
                            th = trL[i].find('th')
                            td = trL[i].find('td')
                            if th is not None and type(th) == type(td) :
                                label = th.get_text()
                                if label=='使用方' or label =='主要用户':
                                    str1 =td.find('a')
                                    if str1 is not None:
                                        content = str1.get_text()
                                if label == '研发者' or label=='设计师':
                                    desinger = td.get_text()
                                    items = item.item(searchItem,0,0,desinger,0)
                                    push.updateItem(items)
                                if label =='参与战争':
                                    warL =td.find_all('a')
                                    for war in warL:
                                        war_name = war.get_text()
                                        items = item.item(searchItem,0,0,0,war_name)
                                        push.saveInIwar(items) 
                        if pattern ==0:
                            td= trL[i].find('td')
                            if td is not None:
                                label = td.get_text()
                                if label == '主要用户':
                                    str2 = td.findNext('td')
                                    content = str2.get_text()
                                if label == '研发者' or label=='设计师':
                                    desinger = td.get_text()
                                    items = item.item(searchItem,0,0,desinger,0)
                                    push.updateItem(items)
                                if label =='参与战争':
                                    warL =td.find_all('a')
                                    for war in warL:
                                        war_name = war.get_text()
                                        items = item.item(searchItem,0,0,0,war_name)
                                        push.saveInIwar(items) 
                        if content!='':
                            ct = content
                            ct.strip()
                            if ct == '使用国' or ct == '使用国家和地区' :
                               address = textlist.find_all(text=ct)
                               l = len(address)
                               h2 = address[l-1].parent
                               ul_tag = h2.findNext('ul')
                               if ul_tag is not None:
                                    li_tag = ul_tag.find_all('li')
                                    if li_tag is not None:
                                        for li in li_tag:
                                            orgl = li.find_all('a',class_="mw-redirect")
                                            for org in orgl:
                                                name = org.get_text()
                                                items = item.item(searchItem,name,0,0,0)
                                                push.saveInIorg(items)
                                                push.saveInOrg(items)
                            else: 
                                name = content
                                items = item.item(searchItem,name,0,0,0)
                                push.saveInIorg(items)
                                push.saveInOrg(items)
                                

    push.close()

