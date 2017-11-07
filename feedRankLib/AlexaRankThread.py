import threading
from Article import Article
from app import app
from models import FeedArticle
from DuckRankThread import DuckRankThread

class AlexaRankThread(threading.Thread):
    def __init__(self, article_id, url, article_html, published_at, db):
        threading.Thread.__init__(self)
        self.article_id = article_id
        self.url = url
        self.article_html = article_html
        self.published_at = published_at
        self.db = db

    def run(self):
        with app.app_context():
            try:
                alexa_data = urllib.urlopen('http://data.alexa.com/data?cli=10&dat=s&url=%s'%self.url).read()
                alexa_rank = int(re.search(r'<REACH[^>]*RANK="(\d+)"', alexa_data).groups()[0])

            except:
                alexa_rank = -1
            feed_article = FeedArticle.query.filter_by(id=self.article_id).first()

            if feed_article:
                feed_article.rank = alexa_rank
                self.db.session.commit()

                DuckRankThread(self.article_id, self.url, self.article_html, alexa_rank, self.published_at, self.db).start()
