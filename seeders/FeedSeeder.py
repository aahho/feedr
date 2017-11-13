from flask import Flask
import csv, jwt
from App.Repository import store
from models import User, UserDetail
from slugify import slugify
import helpers  
import datetime, urllib, re
import os, requests
from models import *

this_dir, this_filename = os.path.split(__file__)
DATA_PATH = os.path.join(this_dir, "feeds.csv")

def seed():
    with open(DATA_PATH, 'rb') as f:
        reader = csv.reader(f)
        App.query.delete()
        db.session.commit()
        app = App(
            id="f83c2e90-b2a0-4382-acd0-24d98c547a01",
            name="Duck Duck Tech",
            slug=slugify("Duck Duck Tech"),
            description="Technology news",
            token=jwt.encode({'app_name': slugify("Duck Duck Tech")}, 'feed_engine', algorithm='HS256')
        )
        db.session.add(app)
        db.session.commit()
        for row in  reader:
            data = {
                'url' : row[0],
                'category' : row[1],
                'app_id' : "f83c2e90-b2a0-4382-acd0-24d98c547a01"
            }
            requests.post(helpers.get_local_server_url() + "/feeds", json=data)


