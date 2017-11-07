from flask import Flask 
from datetime import datetime
import models
from models import db
from  feedAction.UserRepository import UserRepository
from feedAction.FeedRepository import FeedArticleRepository
from Exceptions.ExceptionHandler import FeedrException

def save_article(user_id, article_id):
	user = UserRepository().get_user_by_id(user_id)
	article = FeedArticleRepository().get_by_article_id(article_id)
	if user is not None and article is not None:
		try:
			user_article = models.UserArticle(
			saved_at=datetime.now(),
			user_id=user.id,
			feed_article_id=article.id
			)
			db.session.add(user_article)
			db.session.commit()
			return True
		except Exception as e:
			raise FeedrException('Duplicate entry', 422)
	raise FeedrException('Invalid user or article id', 422)

def remove_article(user_id, article_id):
	user = UserRepository().get_user_by_id(user_id)
	article = FeedArticleRepository().get_by_article_id(article_id)
	if user is not None and article is not None:
		user_article = models.UserArticle().query.filter(\
			models.UserArticle.user_id==user_id and modles.UserArticle.feed_article_id==article_id\
			).first()
		db.session.delete(user_article)
		db.session.commit()
		return True
	raise FeedrException('Invalid user or article id', 422)

def article_list(user_id):
	user = UserRepository().get_user_by_id(user_id)
	if user is not None:
		return user.transformed_articles()
	raise FeedrException('Invalid User', 422)