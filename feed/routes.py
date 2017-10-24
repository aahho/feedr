from flask import Blueprint, request
from flask import render_template

import feedparser

from Controllers import FeedController
from models import *

feed = Blueprint('feed', __name__, template_folder='templates')

@feed.route('/feed', methods = ["GET", "POST"])
def index():
	if request.method == 'POST':
		feed_url = request.form.get('url')
		tags = request.form.getlist('tags')
		return FeedController.store(feed_url, tags)
		feed = feedparser.parse(feed_url)

		if len(feed.entries) <= 0:
			pass
		if len(feed.entries) > 0:
			# save to db
			title = feed.feed.title
			if 'icon' in feed.feed:
				icon = feed.feed.icon
			elif 'image' in feed.feed:
				icon = feed.feed.image.href

			newFeed = Feed(
				title=title,
				url='',
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

		# return "Done"
		return render_template('add_url_page.html', feed = feed)

	return render_template('add_url_page.html')