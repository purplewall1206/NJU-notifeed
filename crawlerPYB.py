import requests
from bs4 import BeautifulSoup
import datetime
import PyRSS2Gen

import sys
sys.path.append('./')
from news import news
from news import newslist

def genDesc(url=''):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="html5lib")
    article = soup.find_all("div",class_='middleside')
    return str(article[0])



def pyb_crawler():
    # newslist = []
    newsUrlPrefix = 'http://pyb.nju.edu.cn/'
    r = requests.get('http://pyb.nju.edu.cn/shownoticelist.action', timeout=5)
    soup = BeautifulSoup(r.text,features="html5lib")
    
    nlist = soup.find_all('li')
    nlist = nlist[13:] # top 5 <li> are outer links
    for link in nlist:
        taga = link.a
        if link.span == None:
            tmpdate = ''
        else :
            tmpdate = str(link.span.text).strip()
        url = newsUrlPrefix+str(taga.get('href'))
        N = news(
            title = str(taga.text),
            date = tmpdate,
            description = genDesc(url),
            href = url,
        )
        newslist.append(N.genRSSItem())

