import csv
from App.Repository import store
from models import User, UserDetail
import helpers  
import datetime
import os
from models import *

this_dir, this_filename = os.path.split(__file__)
DATA_PATH = os.path.join(this_dir, "tech_feeds.csv")

def seed():
    with open(DATA_PATH, 'rb') as f:
        reader = csv.reader(f)
        App.query.delete()
        db.session.commit()
        app = App(
            id=1,
            name="Duck Duck Tech",
            slug="duck_duck_tech",
            description="Technology news"
        )
        db.session.add(app)

        for row in  reader:
            url = row[0]
            existing_feed = Feed.query.filter(Feed.url.ilike(r"%{}%".format(url))).first()
            newFeed = Feed(
                title='',
                url=url,
                app_id=1,
                rss_url=url,
                icon=''
            )
            db.session.add(newFeed)
        db.session.commit()

