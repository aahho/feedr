from flask import render_template, jsonify
from feedfinder2 import find_feeds
import feedparser
from models import *
from slugify import slugify
from feedRankLib.Article import Article
from App.Response import *
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

def store(request):
    url = request.json.get('url')
    # tags = request.json.getlist('tags')
    app_id = request.json.get('app_id')
    url = url.strip()
    feed = feedparser.parse(url)
    if not feed.entries:
        feed_urls = find_feeds(url)
        if feed_urls:
            feed = feedparser.parse(feed_urls[0])
            feed_url = feed_urls[0]
        else :
            return jsonify({'error' : 'Invalid feed url'})
    else : 
        feed_url = url

    existing_feed = Feed.query.filter(Feed.url.ilike(r"%{}%".format(url))).first()
    if not existing_feed:
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
            app_id=app_id,
            rss_url=feed_url,
            icon=icon
        )
        db.session.add(newFeed)
        db.session.commit()

        return respondWithItem(newFeed)

    return jsonify({'error' : 'Feed already added.'})

def destroy(feed_id):
    feed = Feed.query.get(feed_id)
    if feed:
        db.session.delete(feed)
        db.session.commit()
        return jsonify({'success': 'Deleted'})
    return jsonify({'error' : 'Failed to delete feed.'})


