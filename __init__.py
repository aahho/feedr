from flask import Flask, Blueprint, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from Exceptions.ExceptionHandler import FeedrException
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
app.config.from_pyfile('env.py')
db = SQLAlchemy(app)

from Http.routes import base
from Admin.routes import admin
from Auth.routes import auth
from feed.routes import feed
from feedAction.routes import feed_action
from worker.routes import worker

app.register_blueprint(base)
app.register_blueprint(admin, url_prefix = '/admin')
app.register_blueprint(feed)
app.register_blueprint(feed_action)
app.register_blueprint(auth)
app.register_blueprint(worker)

# custome handler
@app.errorhandler(FeedrException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response