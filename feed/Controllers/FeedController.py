from flask import render_template
from feedfinder2 import find_feeds
import feedparser
from models import *
from slugify import slugify
from feedRankLib.Article import Article
import thread
from app import app
from feed.FeedRepository import FeedArticleRepository

def filter_feed(data):
	feedArticleRepo = FeedArticleRepository()
	if 'keywords' in data:
		filterKeys = {
			'keywords' : data['keywords']
		}
	else : 
		filterKeys = {}
	return feedArticleRepo.filter(filterKeys, data['item'], data['page'])

def get_article_details(id):
	feedArticleRepo = FeedArticleRepository()
	return feedArticleRepo.get_by_id(id)

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
			db.session.commit()

		links = [entry.link for entry in feed.entries]
		FeedArticle.query.filter(FeedArticle.url.notin_(links)).filter(FeedArticle.feed_id == newFeed.id).delete(synchronize_session=False)

		for entry in feed.entries:
			title = entry.title
			url = entry.link
			content = entry.summary
			author = entry.author if 'author' in entry else None

			newFeedArticle = FeedArticle(
				title=title,
				url=url,
				content=content,
				author=author,
				feed_id=newFeed.id
			)
			db.session.add(newFeedArticle)
			db.session.commit()

			thread.start_new_thread(get_article_details, (newFeedArticle.id, url))
	return render_template('add_url_page.html', feed = feed)

def get_article_details(id, url):
	with app.app_context():
		articleDetails = Article(url)
		try:
			meta = articleDetails.build_article_meta()
		except:
			print "here"
			FeedArticle.query.filter(FeedArticle.id == id).delete(synchronize_session=False)
			return
		# print meta

		article = FeedArticle.query.filter_by(id=id).first()

		article.rank = meta['rank'], 
		article.share_count = meta['share_count'], 
		article.keywords = meta['keywords'], 
		article.image = meta['image'], 
		article.summary = meta['summary'], 
		article.sentiment = meta['sentiment'], 

		newFeedArticleDetail = FeedArticleDetail(
			title=meta['title'],
			content=meta['content'],
			feed_article_id=article.id
		)
		db.session.add(newFeedArticleDetail)
		db.session.commit()

	print "Done"

