from flask import render_template
from feedfinder2 import find_feeds
import feedparser
from models import *

def store(url, tags):
	feed = feedparser.parse(url)

	if len(feed.entries) <= 0:
		feed_urls = find_feeds(url)
		if len(feed_urls) > 0:
			feed = feedparser.parse(feed_urls[0])
			feed_url = feed_urls[0]
		else :
			return render_template('add_url_page.html', error = {'error' : 'Invalid Link'})
	else : 
		feed_url = url

	if len(feed.entries) > 0:
		# save to db
		title = feed.feed.title
		if 'icon' in feed.feed:
			icon = feed.feed.icon
		elif 'image' in feed.feed:
			icon = feed.feed.image.href
		else :
			icon = None

		newFeed = Feed(
			title=title,
			url=url,
			rss_url=feed_url,
			icon=icon
		)
		db.session.add(newFeed)
		db.session.commit()

		for entry in feed.entries:
			title = entry.title
			url = entry.link
			content = entry.summary
			author = entry.author if 'author' in entry else ''

			newFeedArticle = FeedArticle(
				title=title,
				url=url,
				content=content,
				author=author,
				feed_id=newFeed.id
			)
			db.session.add(newFeedArticle)
			db.session.commit()
	return render_template('add_url_page.html', feed = feed)
