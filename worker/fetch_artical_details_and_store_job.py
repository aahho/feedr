from flask import Flask 
import get_link_data
from App.Repository import *
from models import *

def get_urls():
	urls = fetchAll(FeedArticle, ['url'])
	print urls[0].id
	return {'worked' : 'worked'}

	
