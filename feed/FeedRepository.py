from models import *
from App.Repository import *
# from flask.ext.sqlalchemy import get_debug_queries

class FeedRepository():
 	"""docstring for FeedRepository"""
 	def addFeed(self, data):
 		pass

 	def list():
 		pass

 	def getFeedById(self, id):
 		pass

class CategoryRepository():
	"""docstring for CategoryRepository"""
	def addCategory(self, data):
		pass

class FeedArticleRepository():
	"""docstring for FeedDetailsRepository"""
	def filter(self, filterKeys, item, page):
		return filterByAttributePaginated(FeedArticle, filterKeys, item, page, 'rank', 'asc')

	def get_by_id(self, id):
		return filterByAttribute(FeedArticle, {id : 'id'})