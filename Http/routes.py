from flask import Blueprint, request
from flask import render_template

base = Blueprint('base', __name__, template_folder='templates')

@base.route('/')
def index():
	return render_template('404.html')

