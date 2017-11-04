from __init__ import app
import sys
from feedRankLib import FeedRankJob
from datetime import datetime

start_time = datetime.now()
FeedRankJob().execute()
print datetime.now() - start_time
sys.exit()
