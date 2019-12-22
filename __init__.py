#coding=utf-8
import re
import requests
from bs4 import BeautifulSoup
from CrawlerS import item
from CrawlerS import Connect

class webCrawlerBaiduBaike(object):
    """docstring for webCrawlerBaiduBaike"""
    def __init__(self, url = 'http://baike.baidu.com/search/word'):
        super(webCrawlerBaiduBaike, self).__init__()
        self.url = url
    # input keyword
    # output resquests object
    # url = 'http://baike.baidu.com/search/word'
    def search(self, searchItem):
        word = self.getWordClean(searchItem)
        user_agent ='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        headers = {'User_Agent': user_agent}
        sessions = requests.session()
        sessions.headers = headers
        res = sessions.get(self.url,  params={'word':word},allow_redirects=True)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.content, 'lxml')
 
        # 查找不到词条，那么对返回的搜索列表进行二次查询
        if res.url[:35] == "http://baike.baidu.com/search/none?":
            for soup in self.findInSuggestList(word, soup):
                yield soup
 
        # 直接进入词条
        else:
            # isDrug, drugCharacterIncluded = findCharacterFromHtml(soup)
            yield soup
 
 
    def getWordClean(self, word):
 
        word = re.sub("\((.*)\)", "", word)
        word = word.replace(u"★", "")
        return word
 
 
    # 直接查询不到条目时，百度会返回推荐条目列表。本程序会在推荐条目列表中尝试搜索合适的条目
    def findInSuggestList(self, word, soup):
 
        linkList = soup.find_all('a',class_ = 'result-title')
 
        for link in linkList:
            ajdustedItemName = link.text.replace('_百度百科',"")
            iPos = word.find(ajdustedItemName)
            # 找到最可能的匹配条目
            if iPos != -1:
                # 获得该条目的链接
                tmpUrl = link['href']
                res = requests.get(tmpUrl)
                res.encoding = 'utf-8'
                soup = BeautifulSoup(res.text)
                yield soup
# 使用方法 | example for using
if __name__ == '__main__':
    push = Connect.Connect()
    cL=push.getCountry()
    for i in range(6,len(cL)):
        searchItem = cL[i][0]
        print(i)
        crawler = webCrawlerBaiduBaike()
        soupIter = crawler.search(searchItem)
        isEmpty = True
        article =''
        for soup in soupIter:
            table = soup.find('div',class_="basic-info cmn-clearfix")
            if table is not None:
                textlist1 = table.find_all('dt',class_="basicInfo-item name")
                textlist2 = table.find_all('dd', class_="basicInfo-item value")
                #for each in textlist:
                    #text= each.get_text()
                    #sentence=re.split(pattern=pattern,string=text)
                    #for s in sentence:
                    #    if len(s)>1:
                    #        k = jiagu.knowledge(s)
                    #        if(len(k)>0):
                    #            print(k)        
                    #sentence_seged = jieba.posseg.cut(text.strip())
                    #for x in sentence_seged:
                    #    if x.flag == 'n' or x.flag == 'nr' or x.flag == 'ns' or x.flag == 'nt' or x.flag == 'nz':
                            
                for i in range (0,len(textlist1)):
                    if(textlist1[i].get_text()=='国家领袖'):
                        boss = textlist2[i].get_text()
                        break
                push.updateCountry(boss, searchItem)
    push.close()    
    isEmpty = False
    
    if isEmpty:
        print("搜索结果为空")
