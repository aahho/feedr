from flask import Blueprint, request
from flask import render_template

feed = Blueprint('feed', __name__, template_folder='templates')

@feed.route('/')
def index():
	pass