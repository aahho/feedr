from app import app
from models import *
import helpers
import feedparser
import thread
from feedRankLib import Article
import threading
import datetime

from AlexaRankThread import AlexaRankThread

class ArticleDetails(threading.Thread):
    
    def __init__(self, article_id, article_url, published_at, alexa_rank):
        threading.Thread.__init__(self)        
        self.article_id = article_id
        self.alexa_rank = alexa_rank
        self.article_url = article_url
        self.published_at = published_at

    def run(self):
        with app.app_context():
            articleDetails = Article(self.article_url, self.published_at, self.alexa_rank)
            articleDetails.set_article()
            details_exists = FeedArticleDetail.query.filter_by(feed_article_id=self.article_id).first()
            if details_exists:
                return

            try:
                meta = articleDetails.build_article_meta()
                if not meta:
                    article_to_be_deleted = FeedArticle.query.filter(FeedArticle.id == self.article_id).first()
                    if article_to_be_deleted:
                        db.session.delete(article_to_be_deleted)
                        db.session.commit()
                    return
            except:
                article_to_be_deleted = FeedArticle.query.filter(FeedArticle.id == self.article_id).first()
                db.session.delete(article_to_be_deleted)
                db.session.commit()
                return 

            article = FeedArticle.query.filter_by(id=self.article_id).first()

            article.share_count = meta['share_count'] 
            article.keywords = meta['keywords'] 
            article.image = meta['image'] 
            article.summary = meta['summary'] 
            article.sentiment = meta['sentiment'] 

            newFeedArticleDetail = FeedArticleDetail(
                id=helpers.generate_unique_code(),
                title=meta['title'],
                content=meta['content'],
                feed_article_id=article.id
            )
            db.session.add(newFeedArticleDetail)
            db.session.commit()

            AlexaRankThread(self.article_id, self.article_url, meta['article_html'], self.published_at, self.alexa_rank, db).start()
            db.session.close()

class FeedRankJob:
    def __init__(self):
        self.set_feeds()

    def set_feeds(self):
        self.feeds = Feed.query.all()

    def extract_data(self, feed):
        parsed_feed = feedparser.parse(feed.rss_url)
        links = [entry.link for entry in parsed_feed.entries]

        threads = []

        for entry in parsed_feed.entries:
            existing_article = FeedArticle.query.filter(FeedArticle.url == entry.link).first()
            if existing_article is None :
                newFeedArticle = FeedArticle(
                    id=helpers.generate_unique_code(),
                    title=entry.title,
                    url=entry.link,
                    content=entry.summary,
                    author=entry.author if 'author' in entry else None,
                    published_at=entry.published if 'published' in entry else datetime.datetime.now(),
                    feed_id=feed.id
                )
                db.session.add(newFeedArticle)
                db.session.commit()
            else :
                newFeedArticle = existing_article

            threads.append(ArticleDetails(newFeedArticle.id, newFeedArticle.url, newFeedArticle.published_at, feed.alexa_rank))

        for t in threads:
            t.start()
        for t in threads:
            t.join(20)

    def execute(self):
        for feed in self.feeds:
            self.extract_data(feed)
