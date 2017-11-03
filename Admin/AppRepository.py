from flask import Flask 
from App.Repository import *

class AppRepository():
	"""docstring for AppRepository"""
	def update_app(self, model, app_id, data):
		return update(model, {'id' : app_id}, data)

	def delete_app(self, model, app_id):
		return delete(model, {'id' : app_id})