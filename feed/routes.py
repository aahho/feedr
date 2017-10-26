from flask import Blueprint, request
from flask import render_template
from App.Response import *
import feedparser

from Controllers.FeedController import *
from models import *

feed = Blueprint('feed', __name__, template_folder='templates')

@feed.route('/feeds', methods = ["GET", "POST"])
def index():
	if request.method == 'POST':
		feed_url = request.form.get('url')
		tags = request.form.getlist('tags')
		return store(feed_url, tags)

	return render_template('add_url_page.html')

@feed.route('/feeds/articles/filter', methods = ['GET'])
def filter():
	data = request.args
	response = filter_feed(data)
	return respondWithPaginatedCollection(response)

@feed.route('/feeds/articles/<id>', methods = ['GET'])
def get_artical(id):
	response = get_article_details(id)
	if response:
		return respondWithItem(response)
	return respondWithError('Not Found')