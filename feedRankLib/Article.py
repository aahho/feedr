from textblob import TextBlob
import newspaper, urllib, re
import socialshares, time
from DuckRank import DuckRank

class Article:
    def __init__(self, url, published_at, alexa_rank):
        self.url = url
        self.alexa_rank = alexa_rank
        self.published_at = published_at
        # self.set_article()   
        self.shares = []

    def set_article(self):
        try:
            self.article = newspaper.Article(self.url, keep_article_html=True)
        except Exception as e:
            print e.message

        self.article.download()
        self.article.parse()
        if not self.article.is_parsed:
            time.sleep(1)
        self.article.nlp()
        # self.article.build()

    def get_article(self):
        return self.article

    def build_article_meta(self):
        if not self.article.is_valid_body():
            return False

        return {
            'article': self.article,
            'title': self.article.title,
            'content': self.article.text,
            'article_html': self.article.article_html,
            'image': self.article.top_image,
            'summary': self.article.summary,
            'movies': self.article.movies,
            'keywords': self.get_keywords(),
            'authors': self.article.authors,
            'rank': self.alexa_rank,
            'share_count': self.get_share_count(),
            'duck_rank' : 1, #self.calculate_duck_rank(),
            'sentiment': self.calculate_sentiment(),
        }
    def get_keywords(self):

        return ', '.join(self.article.keywords)

    def calculate_rank(self):
        try:
            alexa_data = urllib.urlopen('http://data.alexa.com/data?cli=10&dat=s&url=%s'%self.url).read()
            return int(re.search(r'<REACH[^>]*RANK="(\d+)"', alexa_data).groups()[0])

        except:
            return -1    

    def calculate_sentiment(self): 
        sentiment = TextBlob(self.article.text).sentiment
        if sentiment.polarity >= 0.1:                                           
            return 1
        elif sentiment.polarity <= -0.1:                                        
            return -1                                          
        else:                                                                   
            return 0

    def calculate_duck_rank(self):
        return DuckRank(self.url, self.article, self.calculate_rank(), self.published_at).calculate()
        
    def get_share_count(self):
        self.shares = socialshares.fetch(self.url, ['facebook', 'pinterest', 'google', 'linkedin', 'reddit'])
        return (self.shares['reddit']['ups'] if 'reddit' in self.shares else 0) \
            + (self.shares['facebook']['share_count'] if 'facebook' in self.shares else 0) \
            + (self.shares['google'] if 'google' in self.shares else 0) \
            + (self.shares['pinterest'] if 'pinterest' in self.shares else 0) \
            + (self.shares['linkedin'] if 'linkedin' in self.shares else 0)
