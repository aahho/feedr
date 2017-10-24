from newspaper import Article
from textblob import TextBlob
import sys, urllib, re

url = sys.argv[1]
article = Article(url)
article.download()
article.parse()
article.nlp()

title = article.title
content = article.text
keywords = article.keywords

xml = urllib.urlopen('http://data.alexa.com/data?cli=10&dat=s&url=%s'%url).read()
try: 
	rank = int(re.search(r'<POPULARITY[^>]*TEXT="(\d+)"', xml).groups()[0])
except: 
	rank = -1

blob = TextBlob(content)
sentiment = blob.sentiment
if sentiment.polarity >= 0.1:
	sentiment = 'positive'
elif sentiment.polarity <= -0.1:
	sentiment = 'negative'
else:
	sentiment = 'neutral'

print 'Title: ', title
print 'Rank: ', rank
print 'Keywords: ', keywords
print 'Sentiment: ', 'positive'   
# print 'Content: ', content
