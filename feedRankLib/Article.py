from textblob import TextBlob
import newspaper, urllib, re
import socialshares
from helpers import duck_rank_algo

class Article:
    def __init__(self, url, published_at):
        self.url = url
        self.published_at = published_at
        self.setArticle()   
        self.shares = []
    

    def setArticle(self):
        self.article = newspaper.Article(self.url)
        self.article.download()
        self.article.parse()
        self.article.nlp()  

    def build_article_meta(self):
        return {
            'title': self.article.title,
            'content': self.article.text,
            'image': self.article.top_image,
            'summary': self.article.summary,
            'movies': self.article.movies,
            'keywords': self.get_keywords(),
            'authors': self.article.authors,
            'rank': self.calculate_rank(),
            'share_count': self.get_share_count(),
            'duck_rank' : self.calculate_duck_rank(),
            'sentiment': self.calculate_sentiment(),
        }

    def get_keywords(self):
        return ', '.join(self.article.keywords)

    def calculate_rank(self):
        try:
            alexa_data = urllib.urlopen('http://data.alexa.com/data?cli=10&dat=s&url=%s'%self.url).read()
            return int(re.search(r'<REACH[^>]*RANK="(\d+)"', alexa_data).groups()[0])
            return int(re.search(r'<POPULARITY[^>]*TEXT="(\d+)"', alexa_data).groups()[0])

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
        return duck_rank_algo(self.article, self.calculate_rank(), self.shares, self.published_at)
        
    def get_share_count(self):
        self.shares = socialshares.fetch(self.url, ['facebook', 'pinterest', 'google', 'linkedin', 'reddit'])
        return (self.shares['reddit']['ups'] if 'reddit' in self.shares else 0) \
            + (self.shares['facebook']['share_count'] if 'facebook' in self.shares else 0) \
            + (self.shares['google'] if 'google' in self.shares else 0) \
            + (self.shares['pinterest'] if 'pinterest' in self.shares else 0) \
            + (self.shares['linkedin'] if 'linkedin' in self.shares else 0)