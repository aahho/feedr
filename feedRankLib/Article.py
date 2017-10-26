from textblob import TextBlob
import newspaper, urllib, re
import socialshares

class Article:
    def __init__(self, url):
        self.url = url
        self.setArticle()   

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
            'sentiment': self.calculate_sentiment(),
            'share_count': self.get_share_count(),
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

    def get_share_count(self):
        shares = socialshares.fetch(self.url, ['facebook', 'pinterest', 'google', 'linkedin', 'reddit'])

        return (shares['reddit']['ups'] if 'reddit' in shares else 0) \
            + (shares['facebook']['share_count'] if 'facebook' in shares else 0) \
            + (shares['google'] if 'google' in shares else 0) \
            + (shares['pinterest'] if 'pinterest' in shares else 0) \
            + (shares['linkedin'] if 'linkedin' in shares else 0)