#!/usr/local/bin python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Command
from flask_migrate import Migrate, MigrateCommand
from __init__ import app, db
from models import *
from worker.fetch_artical_details_and_store_job import get_urls
from seeders.SeedManager import user_seeder

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

class CronCommand(Command):

	def run(self):
		get_urls()

class SeedCommand(Command):
	def run(self) :
		user_seeder()

manager.add_command('cron', CronCommand)
manager.add_command('seed', SeedCommand)

if __name__ == '__main__':
    manager.run()
