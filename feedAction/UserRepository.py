from flask import Flask 
from App.Repository import *
import models

class UserRepository():
	"""docstring for UserRepository"""
	def get_user_by_id(self, user_id):
		return filter_attribute(models.User, {'id' : user_id}).first()