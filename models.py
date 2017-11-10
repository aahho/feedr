from flask import Flask, json, jsonify
from datetime import datetime, timedelta
from __init__ import db
from sqlalchemy import text, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import ARRAY, array
from helpers import datetime_to_epoch
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.associationproxy import association_proxy

# ALDJEMY_DATA_TYPES = {
#     'UUIDField': lambda field: UUID(),
#     'StringField': lambda field: str()
# }

feed_article_category_table = db.Table('feed_category', db.Model.metadata,
    db.Column('feed_id', db.String, db.ForeignKey('feeds.id')),
    db.Column('categories', db.Integer, db.ForeignKey('categories.id'))
)

class App(db.Model):
    __tablename__ = 'apps'

    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False)
    token = db.Column(db.String)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=func.now(), onupdate=func.now())

    def transform(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'slug' : self.slug,
            'description' : self.description,
            'token' : self.token
        }

class Feed(db.Model):
    __tablename__= 'feeds'

    id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.Text)
    url = db.Column(db.Text)
    rss_url = db.Column(db.Text)
    app_id = db.Column(db.ForeignKey(u'apps.id', ondelete=u'CASCADE'), nullable=False)
    icon = db.Column(db.Text)
    domain=db.Column(db.String(100))
    alexa_rank=db.Column(db.Integer)
    feed_updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, onupdate=func.now(), default=func.now())

    categories = db.relationship(
        "Category",
        secondary=feed_article_category_table,
        back_populates="feeds")

    def transform(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'url' : self.rss_url,
            'icon' : self.icon,
            'alexa_rank' : self.alexa_rank,
        }

class FeedArticle(db.Model):
    __tablename__= 'feed_articles'

    id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.Text)
    url = db.Column(db.Text)
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    rank = db.Column(db.Integer)
    duck_rank = db.Column(db.Float)
    share_count = db.Column(db.Integer)
    keywords = db.Column(db.Text)
    image = db.Column(db.Text)
    summary = db.Column(db.Text)
    sentiment = db.Column(db.SmallInteger)
    feed_id = db.Column(db.ForeignKey(u'feeds.id', ondelete=u'CASCADE'), nullable=False)
    # clustered_article = db.Column(ARRAY(db.Text), default=db.cast(array([], type_=db.Text), ARRAY(db.Text)))
    published_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, onupdate=func.now(), default=func.now())

    article_details = relationship(u'FeedArticleDetail', uselist=False, back_populates="feed_article")
    # article_users = relationship("UserArticle", back_populates="user_articles")
    users = relationship("UserArticle", back_populates="articles")
    

    def duck_rank_percentile(self, duck_rank):
        max_rank = db.session.query(func.max(FeedArticle.duck_rank)).scalar()
        return (duck_rank / max_rank) * 100

    def max_duck_rank(self):
        r = db.session.query(func.max(FeedArticle.duck_rank)).scalar()
        return r if r else 0

    def minimal_transformer(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'duckRank' : self.duck_rank_percentile(self.duck_rank),
            'publishedAt' : datetime_to_epoch(self.published_at),
        }

    def mini_transformer(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'url' : self.url,
            'rank' : self.rank,
            'duckRank' : self.duck_rank_percentile(self.duck_rank),
            'shareCount' : self.share_count,
            'image' : self.image,
            'keywords' : self.keywords.split(',') if self.keywords is not None else [],
            'publishedAt' : datetime_to_epoch(self.published_at),
            'updatedAt' : datetime_to_epoch(self.updated_at)
        }

    def transform(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'url' : self.url,
            'content' : self.content,
            'duckRank' : self.duck_rank,
            'rank' : self.rank,
            'keywords' : self.keywords.split(',') if self.keywords is not None else [],
            'image' : self.image,
            'summary' : self.summary,
            'sentiment' : self.sentiment,
            'feedId' : self.feed_id,
            'duckRank' : self.duck_rank_percentile(self.duck_rank),
            'shareCount' : self.share_count,
            'details' : self.article_details.transform() if self.article_details != None else None,
            'publishedAt' : datetime_to_epoch(self.published_at),
            'updatedAt' : datetime_to_epoch(self.updated_at)     
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
    
    id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    rich_rank = db.Column(db.Integer)
    country_code = db.Column(db.String(255))
    country_name = db.Column(db.String(255))
    country_rank = db.Column(db.Integer)
    movie = db.Column(ARRAY(db.Text), default=db.cast(array([], type_=db.Text), ARRAY(db.Text)))
    feed_article_id = db.Column(db.ForeignKey(u'feed_articles.id', ondelete=u'CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, onupdate=func.now(), default=func.now())

    feed_article = relationship("FeedArticle", back_populates="article_details")
    
    def transform(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'content' : self.content,
            'rich_rank' : self.rich_rank,
            'countryCode' : self.country_code,
            'countryName' : self.country_name,
            'movie' : self.movie,
        }

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(100), primary_key=True)
    display_name = db.Column(db.String(70))
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(60))
    reset_pin = db.Column(db.SmallInteger, nullable=False, server_default=text("(0)::smallint"))
    is_banned = db.Column(db.Boolean, nullable=False, server_default=text("false"))
    is_god = db.Column(db.Boolean, nullable=False, server_default=text("false"))
    is_active = db.Column(db.Boolean, nullable=False, server_default=text("false"))
    confirmation_code = db.Column(db.String(255))
    last_login_location = db.Column(db.JSON)
    is_password_change_required = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=func.now(), onupdate=func.now())
    slack_id = db.Column(db.String(30))
    logo = db.Column(db.Text)
    is_premium_user = db.Column(db.Boolean, server_default=text("false"))

    articles = relationship("UserArticle", back_populates="users")

    def transformed_articles(self):
        user_articles = []
        for article in self.articles:
            user_articles.append(article.article_transformer())
        return user_articles

    def transform(self):
        return {
            'id' : self.id,
            'displayName' : self.display_name,
            'email' : self.email,
            'isGod' : self.is_god,
            'isBanned' : self.is_banned,
            'isPremiumUser' : bool(self.is_premium_user),
            'articles' : self.transformed_articles(),
            # 'lastLoginLocation' : self.last_login_location
        }


class UserDetail(db.Model):
    __tablename__ = 'user_details'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(u'users.id', ondelete=u'CASCADE'), nullable=False)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    country = db.Column(db.String(40))
    state = db.Column(db.String(40))
    city = db.Column(db.String(40))
    mobile_number = db.Column(db.String(15))
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=func.now(), onupdate=func.now())
    location = db.Column(db.JSON)

    user = relationship(u'User')

def expires_at():
    return datetime.utcnow() + timedelta(days=7)

class UserToken(db.Model):
    __tablename__ = 'user_tokens'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(u'users.id', ondelete=u'CASCADE'), nullable=False)
    token = db.Column(db.String(100), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False,  default=expires_at)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=func.now(), onupdate=func.now())

    user = relationship(u'User')

    def transform(self):
        return {
            'id' : self.id,
            'token' : self.token,
            'expiresAt' : datetime_to_epoch(self.expires_at),
            'user' : self.user.transform()
        }

class UserArticle(db.Model):
    """docstring for UserArticle"""
    __tablename__ = 'user_articles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey(u'users.id'))
    feed_article_id = db.Column(db.String, db.ForeignKey(u'feed_articles.id'))
    saved_at = db.Column(db.DateTime)

    __table_args__ = (
        UniqueConstraint("user_id", "feed_article_id"),
    )

    users = relationship('User',  back_populates='articles')
    articles = relationship('FeedArticle', back_populates='users')

    def article_transformer(self):
        return {
            'savedAt' : datetime_to_epoch(self.saved_at),
            'article' : self.articles.minimal_transformer()
        }