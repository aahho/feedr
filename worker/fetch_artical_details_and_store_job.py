from flask import Flask
import get_link_data
from feed.FeedRepository import *
from feed.Controllers.FeedController import *
from models import *
from feedRankLib import Article
from datetime import datetime
from dateutil.parser import parse

def get_urls():
    # f = open('/Users/probir/Code/aahho/feedr/test.txt', 'a')
    # f.write('Worked\n')
    # f.close()
    # return "ok"
    # rss = FeedRepository().list_feeds()
    # for feed in rss:
    article = Article("https://www.nytimes.com/2017/10/27/health/medicaid-maine-obamacare.html?partner=rss&emc=rss",\
    	datetime.now())
    article.build_article_meta()
    # data = artical_details("https://www.nytimes.com/2017/10/27/health/medicaid-maine-obamacare.html?partner=rss&emc=rss")
    return "worked"

