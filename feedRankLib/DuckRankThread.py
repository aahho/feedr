import threading
from DuckRank import DuckRank
from app import app
from models import FeedArticle

class DuckRankThread(threading.Thread):

    def __init__(self, article_id, url, article, alexa_rank, published_at, db):
        threading.Thread.__init__(self)
        self.article_id = article_id
        self.url = url
        self.article = article
        self.alexa_rank = alexa_rank
        self.published_at = published_at
        self.db = db

    def run(self):
        with app.app_context():
            duck_rank = DuckRank(self.url, self.article, self.alexa_rank, self.published_at)
            rank = duck_rank.calculate()
            feed_article = FeedArticle.query.filter_by(id=self.article_id).first()
            if feed_article:
                feed_article.duck_rank = rank
                self.db.session.commit()

