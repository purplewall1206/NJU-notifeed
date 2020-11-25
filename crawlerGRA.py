# coding: utf8
mport requests
import sys
from bs4 import BeautifulSoup
import datetime
import PyRSS2Gen
import sys
sys.path.append('/home/wangzc/Documents/notifeed')
from news import news
from news import newslist

def genDesc(url=''):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="html5lib")
    article = soup.find_all("div",class_="article")
    # print(str(article[0]))
    return str(article[0])


def gra_crawler():
    # newslist = []
    newsUrlPrefix = 'https://grawww.nju.edu.cn'
    r = requests.get('https://grawww.nju.edu.cn/905/list.htm', timeout=5)
    soup = BeautifulSoup(r.text,features="html5lib")
    

    nlist = soup.find_all('li')
    item_list = []
    for link in nlist:
        if link['class'][0] == 'list_item':
            # nlist.append(link)
            item_list.append(link)

    for item in item_list:
        spans = item.find_all('span')
        title = str(spans[1].a.text)
        url = newsUrlPrefix+str(spans[1].a['href'])
        datestr = str(spans[2].text)
        N = news(
            title = title,
            date = datestr,
            description = genDesc(url),
            href = url
        )
        newslist.append(N.genRSSItem())


