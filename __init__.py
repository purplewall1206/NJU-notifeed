import sys
sys.path.append('./')
from crawlerPYB import pyb_crawler
from crawlerGRA import gra_crawler
from news import newslist
from flask import Flask, escape, url_for
import PyRSS2Gen
import datetime
import time
import threading
import logging

logging.basicConfig(format="%(asctime)s %(name)s:%(levelname)s:%(message)s",filename='logger.log',level=logging.INFO)

app = Flask(__name__)

global feed

lock = threading.Lock()

def genFeed():
    while True:
        newslist = []
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
        
        rss.write_xml(open("feed.xml", "w",encoding='UTF-8',errors='ignore'))
        logging.info('generate feed file')
        
        lock.acquire(True)
        global feed 
        with open('feed.xml', "r",encoding='utf8') as f:
            feed = f.read()
        lock.release()
        logging.info('update rss feed')

        time.sleep(1000)



@app.route('/rss')
def rss():    
    RSS = ''
    lock.acquire(True)
    RSS = feed
    lock.release()
    return RSS
    



if __name__ =="__main__":
    
    try:
        threading.Thread(target=genFeed).start()
    except:
        logging.error('thread failure')
    
    app.run('0.0.0.0', debug=False, port=8000)
    # crawl.join()
