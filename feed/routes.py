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

	return render_template('add_url_page.html')