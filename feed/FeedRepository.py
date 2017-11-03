from models import *
from App.Repository import *
# from flask.ext.sqlalchemy import get_debug_queries

class FeedRepository():
 	"""docstring for FeedRepository"""
 	def add_feed(self, data):
 		pass

 	def list_feeds(self):
 		return fetchAll(Feed)

 	def getFeedById(self, id):
 		pass

class CategoryRepository():
	"""docstring for CategoryRepository"""
	def addCategory(self, data):
		pass

class FeedArticleRepository():
	"""docstring for FeedDetailsRepository"""
	def filter(self, filterKeys, item, page):
		return filterByAttributePaginated(FeedArticle, filterKeys, item, page, {'duck_rank': 'desc', 'published_at' : 'desc'})

	def get_by_id(self, id):
		return filterByAttribute(FeedArticle, {id : 'id'})

class FeedArticleDetailRepository():
 	"""docstring for FeedArticleDetailRepository"""

 	def list_article_details(self):
 		return fetchAll(FeedArticleDetail)

