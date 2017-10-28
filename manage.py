from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Command
from flask_migrate import Migrate, MigrateCommand
from __init__ import app, db
from models import *
from worker.fetch_artical_details_and_store_job import get_urls

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

class CronCommand(Command):

	def run(self):
		get_urls()
		print "worked"

manager.add_command('cron', CronCommand)

if __name__ == '__main__':
    manager.run()
