import sys
sys.path.append('./')
from crawlerPYB import pyb_crawler
from crawlerGRA import gra_crawler
from news import newslist
from flask import Flask, escape, url_for
import PyRSS2Gen
import datetime


app = Flask(__name__)

def genFeed():
    pyb_crawler()
    gra_crawler()
    rss = PyRSS2Gen.RSS2(
        title = "南京大学研究生通知",
        link = "https://www.zi-c.wang",
        description = "研究生学籍和研究生院两个网站的feed，每小时更新",
        lastBuildDate = datetime.datetime.now(),
        items = newslist
    )
    rss.write_xml(open("feed.xml", "w"))


feed = ""


@app.route('/rss')
def rss():
    
    return feed


if __name__ =="__main__":
    genFeed()
    with open('feed.xml', "r") as f:
        feed = f.read()
    app.run('0.0.0.0', debug=False, port=8000)
