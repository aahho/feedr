from flask import Flask
import get_link_data
from feed.FeedRepository import *
from feed.Controllers.FeedController import *
from models import *
import datetime

def get_urls():
    rss = FeedRepository().list_feeds()
    for feed in rss:
        data = store(feed.url, [])
    return "worked"

