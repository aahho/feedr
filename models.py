from flask import Flask
from __init__ import db
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ARRAY, array

feed_article_category_table = db.Table('feed_category', db.Model.metadata,
    db.Column('feed_id', db.Integer, db.ForeignKey('feeds.id')),
    db.Column('categories', db.Integer, db.ForeignKey('categories.id'))
)

class Feed(db.Model):
    __tablename__= 'feeds'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    url = db.Column(db.Text)
    rss_url = db.Column(db.Text)
    icon = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, onupdate=func.now(), default=func.now())

    categories = db.relationship(
        "Category",
        secondary=feed_article_category_table,
        back_populates="feeds")

class FeedArticle(db.Model):
    __tablename__= 'feed_articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    url = db.Column(db.Text)
    content = db.Column(db.Text)
    author = db.Column(db.String(70))
    rank = db.Column(db.Integer)
    keywords = db.Column(db.Text)
    image = db.Column(db.Text)
    summary = db.Column(db.Text)
    sentiment = db.Column(db.SmallInteger)
    feed_id = db.Column(db.ForeignKey(u'feeds.id', ondelete=u'CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, onupdate=func.now(), default=func.now())

    def transform(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'url' : self.url,
            'content' : self.content,
            'author' : self.author,
            'feed_id' : self.feed_id
        }

class Category(db.Model):
    __tablename__= 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, onupdate=func.now(), default=func.now())

    feeds = db.relationship(
        "Feed",
        secondary=feed_article_category_table,
        back_populates="categories")

class FeedArticleDetail(db.Model):
    """docstring for FeedArticalDetail"""
    __tablename__= 'feed_article_details'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    rank = db.Column(db.Integer)
    content = db.Column(db.Text)
    rich_rank = db.Column(db.Integer)
    country_code = db.Column(db.String(255))
    country_name = db.Column(db.String(255))
    country_rank = db.Column(db.Integer)
    author = db.Column(ARRAY(db.Text), nullable=False, default=db.cast(array([], type_=db.Text), ARRAY(db.Text)))
    feed_id = db.Column(db.ForeignKey(u'feeds.id', ondelete=u'CASCADE'), nullable=False)
    feed_article_id = db.Column(db.ForeignKey(u'feed_articles.id', ondelete=u'CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, onupdate=func.now(), default=func.now())
        
