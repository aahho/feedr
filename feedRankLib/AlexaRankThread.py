import threading
from Article import Article
from app import app
from models import FeedArticle
from DuckRankThread import DuckRankThread

class AlexaRankThread(threading.Thread):
    def __init__(self, article_id, url, article_html, published_at, alexa_rank, db):
        threading.Thread.__init__(self)
        self.article_id = article_id
        self.alexa_rank = alexa_rank
        self.url = url
        self.article_html = article_html
        self.published_at = published_at
        self.db = db

    def run(self):
        with app.app_context():
            feed_article = FeedArticle.query.filter_by(id=self.article_id).first()

            if feed_article:
                feed_article.rank = self.alexa_rank
                self.db.session.commit()

                DuckRankThread(self.article_id, self.url, self.article_html, self.alexa_rank, self.published_at, self.db).start()
