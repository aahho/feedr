from flask import Blueprint, request
from flask import render_template
from App.Response import *
import feedparser
from decorators import validate_jwt_token

from Controllers.FeedController import *
from models import *

feed = Blueprint('feed', __name__, template_folder='templates')

@feed.route('/feeds', methods = ["POST"])
def index():
	if request.method == 'POST':
		return store(request)

@feed.route('/feeds/<feed_id>', methods = ["DELETE"])
def delete(feed_id):
    return destroy(feed_id)

@feed.route('/feeds/articles/filter', methods = ['GET'])
@validate_jwt_token
def filter():
	data = request.args
	app_id = request.app.get('id')
	response = filter_feed(data, app_id)
	return respondWithPaginatedCollection(response, 'mini_transformer')

@feed.route('/feeds/articles/<id>', methods = ['GET'])
@validate_jwt_token
def get_artical(id):
	response = get_article_data(id)
	if response:
		return respondWithItem(response)
	return respondWithError('Not Found')
