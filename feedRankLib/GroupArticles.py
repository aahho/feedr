from flask import Flask 
from models import *
from feed.FeedRepository import FeedArticleDetailRepository
from SentenceSimilarity import similarity
import threading
import time

def group_articles():
	article_details = FeedArticleDetailRepository().list_article_details()
	for art in article_details:
		for art1 in article_details:
			group_content(art, art1)
			# break
			print art1.title, '/////',  art.title
			# group_content(art1, article_details[2])
			# break
			# print threading.Thread(target=group_content, args=(art, art1)).start()
			# print "sleeping"
			# time.sleep(10)
			# print "woke up"
			# break
		# break

def group_content(art, art1):
	similarity = check_similarity(art.content, art1.content, True)
	
	print similarity

def check_similarity(text1, text2, info_content_norm=True):
	return similarity(text1, text2, True)