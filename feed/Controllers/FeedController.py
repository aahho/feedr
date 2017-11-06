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

def filter_feed(data, app_id):
    feedArticleRepo = FeedArticleRepository()
    query = FeedArticle.query
    feed_ids = FeedRepository().get_id_list({'app_id' : app_id})
    query = query.filter(FeedArticle.feed_id.in_(feed_ids))

    if 'domain' in data:
        feed_ids = Feed.query.filter(Feed.domain.ilike('%'+data['domain']+"%")).options(load_only('id')).all()
        f_ids = []
        for feed_id in feed_ids:
            f_ids.append(feed_id.id)
        if f_ids is not []:
            query = query.filter(FeedArticle.feed_id.in_(f_ids))
            

    # query = query.filter(FeedArticle.feed_id.in_(feed_id))
    if 'keywords' in data:
        keys = data['keywords'].split(',')
        r = []
        for key in keys:
            r.append(FeedArticle.keywords.ilike('%'+key+'%'))
            #r.append(or_(FeedArticle.keywords.ilike('%, ' + key.strip() + ',%'), \
            #    FeedArticle.keywords.ilike(key.strip() + ',%')))
        query = query.filter(or_(*r))
    
    if 'duck_rank' in data:
        max_duck_rank = FeedArticle().max_duck_rank()
        duck_rank = (max_duck_rank * int(data['duck_rank']))/100
        query = query.filter(FeedArticle.duck_rank >= duck_rank).order_by(desc(FeedArticle.duck_rank))
    
    if 'd_min' in data and 'd_max' in data:
        query = query.filter(FeedArticle.published_at.between(\
            datetime.datetime.now() - datetime.timedelta(days=int(data['d_max'])),\
            datetime.datetime.now() - datetime.timedelta(days=int(data['d_min']))))
    if 'd' in data:
        if data['d'] is not 0:
            query = query.filter(FeedArticle.published_at >= datetime.datetime.now() - datetime.timedelta(days=int(data['d']))) 
            
    query = query.order_by(desc(FeedArticle.published_at))
    return feedArticleRepo.filter(query, data['item'] if 'item' in data else 10, data['page'] if 'page' in data else 1)

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
        print feed_urls
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

def destroy(feed_id):
    feed = Feed.query.get(feed_id)
    if feed:
        db.session.delete(feed)
        db.session.commit()
        return jsonify({'success': 'Deleted'})
    return jsonify({'error' : 'Failed to delete feed.'})


