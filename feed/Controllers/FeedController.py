from flask import render_template
from feedfinder2 import find_feeds
import feedparser
from models import *
from slugify import slugify
from feedRankLib.Article import Article
import thread
from app import app
from feed.FeedRepository import FeedArticleRepository

def filter_feed(data):
    feedArticleRepo = FeedArticleRepository()
    if 'keywords' in data:
        filterKeys = {
            'keywords' : data['keywords'],
        }
    else : 
        filterKeys = {}
    return feedArticleRepo.filter(filterKeys, data['item'] if 'item' in data else 10, data['page'] if 'page' in data else 1)

def get_article_data(id):
    feedArticleRepo = FeedArticleRepository()
    return feedArticleRepo.get_by_id(id)

def store(url, tags):
    url = url.strip()
    feed = feedparser.parse(url)
    if not len(feed.entries):
        feed_urls = find_feeds(url)
        if len(feed_urls) > 0:
            feed = feedparser.parse(feed_urls[0])
            feed_url = feed_urls[0]
        else :
            return render_template('add_url_page.html', error = {'error' : 'Invalid Link'})
    else : 
        feed_url = url

    existing_url = Feed.query.filter(Feed.url.ilike(r"%{}%".format(url))).first()
    if not existing_url:
        title = feed.feed.title
        if 'icon' in feed.feed:
            icon = feed.feed.icon
        elif 'image' in feed.feed:
            icon = feed.feed.image.href
        else :
            icon = None

        newFeed = Feed(
            title=title,
            url=url,
            rss_url=feed_url,
            icon=icon
        )
        db.session.add(newFeed)
        db.session.commit()

    return render_template('add_url_page.html', success = True)


