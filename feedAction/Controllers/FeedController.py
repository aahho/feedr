from flask import Flask
import feedparser
from models import *
import helpers
from sqlalchemy.orm import load_only
from sqlalchemy import text, or_, desc
import datetime, tldextract
from feedAction.FeedRepository import FeedRepository, FeedArticleRepository

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
    
    if 'title' in data:
        query = query.filter(FeedArticle.title.ilike('%'+data['title']+'%'))

    if 'duck_rank' in data:
        max_duck_rank = FeedArticle().max_duck_rank()
        duck_rank = (max_duck_rank * int(data['duck_rank']))/100
        query = query.filter(FeedArticle.duck_rank >= duck_rank)
    
    if 'sort' in data:
        column = data['sort'].split('.')[0]
        order = data['sort'].split('.')[1]
        query = query.order_by(getattr(getattr(modelName, column), order))
    else:
        query = query.order_by(desc(FeedArticle.published_at))

    if 'd_min' in data and 'd_max' in data:
        query = query.filter(FeedArticle.published_at.between(\
            datetime.datetime.now() - datetime.timedelta(days=int(data['d_max'])),\
            datetime.datetime.now() - datetime.timedelta(days=int(data['d_min']))))
    if 'd' in data:
        if data['d'] is not 0:
            query = query.filter(FeedArticle.published_at >= datetime.datetime.now() - datetime.timedelta(days=int(data['d']))) 
            
    return feedArticleRepo.filter(query, data['item'] if 'item' in data else 10, data['page'] if 'page' in data else 1)

def get_article_data(id):
    feedArticleRepo = FeedArticleRepository()
    return feedArticleRepo.get_by_id(id)
