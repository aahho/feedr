from app import app
from models import *
import feedparser
import thread
from feedRankLib import Article
import threading

class ArticleDetails(threading.Thread):
    
    def __init__(self, article_id, article_url, published_at):
        threading.Thread.__init__(self)        
        self.article_id = article_id
        self.article_url = article_url
        self.published_at = published_at

    def run(self):
        with app.app_context():
            articleDetails = Article(self.article_url, self.published_at)
            try:
                meta = articleDetails.build_article_meta()
            except:
                print "here"
                FeedArticle.query.filter(FeedArticle.id == self.article_id).delete(synchronize_session=False)
                return 

            article = FeedArticle.query.filter_by(id=self.article_id).first()

            article.rank = meta['rank'], 
            article.share_count = meta['share_count'], 
            article.keywords = meta['keywords'], 
            article.image = meta['image'], 
            article.summary = meta['summary'], 
            article.duck_rank = meta['duck_rank'], 
            article.sentiment = meta['sentiment'], 

            newFeedArticleDetail = FeedArticleDetail(
                title=meta['title'],
                content=meta['content'],
                feed_article_id=article.id
            )
            db.session.add(newFeedArticleDetail)
            db.session.commit()

        print "Done"


class FeedRankJob:
    def __init__(self):
        self.set_feeds()

    def set_feeds(self):
        self.feeds = Feed.query.all()

    def extract_data(self, feed):
        parsed_feed = feedparser.parse(feed.rss_url)
        links = [entry.link for entry in parsed_feed.entries]
        FeedArticle.query.filter(FeedArticle.url.notin_(links)).filter(FeedArticle.feed_id == feed.id).delete(synchronize_session=False)

        for entry in parsed_feed.entries:
            existing_article = FeedArticle.query.filter(FeedArticle.url == entry.link).first()
            if existing_article is None :
                newFeedArticle = FeedArticle(
                    title=entry.title,
                    url=entry.link,
                    content=entry.summary,
                    author=entry.author if 'author' in entry else None,
                    published_at=entry.published,
                    feed_id=feed.id
                )
                db.session.add(newFeedArticle)
                db.session.commit()
            else :
                newFeedArticle = existing_article

            ArticleDetails(newFeedArticle.id, newFeedArticle.url, newFeedArticle.published_at).start()

    def execute(self):
        for feed in self.feeds:
            self.extract_data(feed)
