from flask import render_template
from feedfinder2 import find_feeds
import feedparser
from models import *
from slugify import slugify


def store(url, tags):
	url = url.strip()
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
		associated_tags = []

		for tag in tags:
			slug = slugify(tag)
			existing_tag = Category.query.filter(Category.slug == slug).first()
			associated_tags.append(existing_tag)
			if not existing_tag:
				category = Category(
					name=tag,
					slug=slug
				)
				db.session.add(category)
				db.session.commit()
				associated_tags.append(existing_tag)

		# save to db
		existing_url = Feed.query.filter(Feed.url.ilike(r"%{}%".format(url))).first()
		if not existing_url:
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
			newFeed.categories = associated_tags
			db.session.add(newFeed)
			db.session.commit()
		else:
			newFeed = existing_url
			FeedArticle.query.filter_by(feed_id=newFeed.id).delete()
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
