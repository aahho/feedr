from newspaper import Article
from textblob import TextBlob
import sys, urllib, re
	
# url = sys.argv[1]
def artical_details(url):
	article = Article(url)
	article.download()
	article.parse()
	article.nlp()

	title = article.title
	content = article.text
	keywords = article.keywords
	top_image = article.top_image
	movies = article.movies
	authors = article.authors
	summary = article.summary
	rank = None
	rich_rank = None
	country_code = None
	country_name = None
	country_rank = None

	xml = urllib.urlopen('http://data.alexa.com/data?cli=10&dat=s&url=%s'%url).read()

	try: 
		rank = int(re.search(r'<POPULARITY[^>]*TEXT="(\d+)"', xml).groups()[0])
		rich_rank = int(re.search(r'<REACH[^>]*RANK="(\d+)"', xml).groups()[0])
		country_code = (re.search(r'<COUNTRY[^>]*CODE="([A-Z]+)"', xml).groups()[0])
		country_name = (re.search(r'<COUNTRY[^>]*NAME="([A-Z][a-z]+)"', xml).groups()[0])
		country_rank = int(re.search(r'<COUNTRY[^>]*RANK="(\d+)"', xml).groups()[0])
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

	return {
		'title' : title,
		'rank' : rank,
		'keywords' : keywords,
		'sentiment' : sentiment,
		'content' : content,
		'top_image' : top_image,
		'movies' : movies,
		'authors' : authors,
		'rich_rank' : rich_rank,
		'country_code' : country_code,
		'country_name' : country_name,
		'country_rank' : country_rank, 
		'summary' : summary,
	}
	# print 'rich_rank:', rich_rank
	# print 'country_code:', country_code
	# print 'country_name:', country_name
	# print 'country_rank:', country_rank
	# print 'Title: ', title
	# print 'Rank: ', rank
	# print 'Keywords: ', keywords
	# print 'top_image: ', top_image
	# print 'movies: ', movies
	# print 'authors: ', authors
	# print 'Sentiment: ', 'positive'   
	# print 'Content: ', content
