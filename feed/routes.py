from flask import Blueprint, request
from flask import render_template
from App.Response import *
import feedparser
from decorators import validate_jwt_token
from Exceptions.ExceptionHandler import FeedrException
from Controllers.FeedController import *
from models import *

feed = Blueprint('feed', __name__, template_folder='templates')

@feed.route('/feeds', methods = ["POST"])
def index():
	if request.method == 'POST':
		return store(request)

@feed.route('/feeds/keywords', methods = ["GET"])
def get_keywords():
	if request.method == 'GET':
		return respondWithArray(get_keyword_list())

@feed.route('/feeds/categories', methods = ["GET"])
def get_categories():
	if request.method == 'GET':
		response = get_categories_list()
		if response:
			return respondWithCollection(response)
		raise FeedrException('failed to fetch')

@feed.route('/feeds/categories/<cat_id>', methods = ["GET"])
def get_category_by_id(cat_id):
	if request.method == 'GET':
		return respondWithItem(get_categories_by_id(cat_id))


@feed.route('/feeds/<feed_id>', methods = ["DELETE", "PUT"])
def delete(feed_id):
	if request.method == 'PUT':
		return update(feed_id, request)
	return destroy(feed_id)

@feed.route('/latestNews', methods = ['GET'])
def get_latest_news():
	response = fetch_latest_news()
	if response:
		return respondWithItem(response, 'notification_transformer')
	raise FeedrException('No Letest news')
		
