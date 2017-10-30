from flask import Blueprint, request, json, jsonify
from flask import render_template


from fetch_artical_details_and_store_job import *


worker = Blueprint('worker', __name__, template_folder='templates')

@worker.route('/worker', methods = ["GET", "POST"])
def index():
	if request.method == 'GET':
		return get_urls()