from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

db = None


def createApp(app):
	global db 
	db = SQLAlchemy(app)