from flask import Blueprint, request
from flask import render_template

import feedparser

from feed.Controllers import FeedController

feed = Blueprint('feed', __name__, template_folder='templates')

@feed.route('/feed', methods = ["GET", "POST"])
def index():
	if request.method == 'POST':
		feed_url = request.form.get('url')
		tags = request.form.getlist('tags')
		feed = feedparser.parse(feed_url)
		# add data to db

		return render_template('add_url_page.html', feed = feed)

	return FeedController.store()