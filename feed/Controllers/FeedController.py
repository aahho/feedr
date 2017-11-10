from flask import render_template, jsonify
from feedfinder2 import find_feeds
import feedparser
from models import *
import helpers
from slugify import slugify
from feedRankLib.Article import Article
from App.Response import *
from sqlalchemy.orm import load_only
from sqlalchemy import text, or_, desc
import datetime, tldextract
from feed.FeedRepository import FeedRepository, FeedArticleRepository
import thread
from app import app

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
        ext = tldextract.extract(url)
        domain_name = ext.domain + '.' + ext.suffix
        newFeed = Feed(
            id=helpers.generate_unique_code(),
            title=title,
            url=url,
            domain=domain_name,
            app_id=app_id,
            rss_url=feed_url,
            icon=icon
        )
        db.session.add(newFeed)
        db.session.commit()

        return respondWithItem(newFeed)

    return jsonify({'error' : 'Feed already added.'})

def get_keyword_list():
    # sql_quey = 'select string_to_array(keywords, ',') from feed_articles;'
    key_list = []
    keywords = FeedArticle.query.options(load_only('keywords')).all()
    for keyword in keywords:
        if keyword.keywords is not None : 
            key_list.extend(keyword.keywords.split(','))
    return list(set(key_list))

def destroy(feed_id):
    feed = Feed.query.get(feed_id)
    if feed:
        db.session.delete(feed)
        db.session.commit()
        return jsonify({'success': 'Deleted'})
    return jsonify({'error' : 'Failed to delete feed.'})


