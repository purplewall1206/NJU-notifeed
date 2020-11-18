import requests
import sys
from bs4 import BeautifulSoup
import datetime
import PyRSS2Gen
import sys
sys.path.append('/home/wangzc/Documents/notifeed')
from news import news
from news import newslist

newsUrlPrefix = 'http://pyb.nju.edu.cn/'
r = requests.get('http://pyb.nju.edu.cn/shownoticelist.action', timeout=5)
soup = BeautifulSoup(r.text,features="html5lib")

# li->a + span
#   a->title + href
#   span-> date
nlist = soup.find_all('li')
nlist = nlist[13:] # top 5 <li> are outer links
for link in nlist:
    taga = link.a
    if link.span == None:
        tmpdate = ''
    else :
        tmpdate = str(link.span.text).strip()
    N = news(
        title = str(taga.text),
        date = tmpdate,
        description = str(taga.text),
        href = newsUrlPrefix+str(taga.get('href')),
    )
    newslist.append(N.genRSSItem())

rss = PyRSS2Gen.RSS2(
    title = "pyb notification",
    link = "http://pyb.nju.edu.cn/shownoticelist.action",
    description = "test pyb notification",
    lastBuildDate = datetime.datetime.now(),

    items = newslist
)

rss.write_xml(open("test.xml", "w"))
