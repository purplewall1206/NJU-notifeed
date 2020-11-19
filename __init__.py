import sys
sys.path.append('./')
from crawlerPYB import pyb_crawler
from crawlerGRA import gra_crawler
from news import newslist
from flask import Flask, escape, url_for
import PyRSS2Gen
import datetime
import time
import _thread
import logging

logging.basicConfig(format="%(asctime)s %(name)s:%(levelname)s:%(message)s",filename='logger.log',level=logging.INFO)

app = Flask(__name__)
# 线程不安全，不过flask没研究基本黑箱状态，要啥自行车
global feed

def genFeed():
    while True:
        pyb_crawler()
        logging.info('pyb crawler launched')
        gra_crawler()
        logging.info('gra crawler launched')
        rss = PyRSS2Gen.RSS2(
            title = "南京大学研究生通知",
            link = "https://www.zi-c.wang",
            description = "研究生学籍和研究生院两个网站的feed，每小时更新",
            lastBuildDate = datetime.datetime.now(),
            items = newslist
        )

        rss.write_xml(open("feed.xml", "w"))
        logging.info('generate feed file')
        global feed 
        with open('feed.xml', "r") as f:
            feed = f.read()
        logging.info('update rss feed')

        time.sleep(1000)



@app.route('/rss')
def rss():    
    # print(feed)
    return feed


if __name__ =="__main__":
    
    try:
        _thread.start_new_thread(genFeed, ())
    except:
        logging.error('thread failure')
    
    app.run('0.0.0.0', debug=False, port=8000)
    # crawl.join()
