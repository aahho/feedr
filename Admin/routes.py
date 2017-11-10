from flask import Flask, Blueprint, request, session
from flask import render_template, jsonify
from App.Response import *
from Controllers.AuthController import *
from Controllers import AppController
from decorators import api_login_required, login_required

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/')
def index():
    return render_template('admin_login.html')

@admin.route('/appLogin', methods=['POST'])
def app_login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = legacyLogin(email, password)
    return user

@admin.route('/home', methods=['GET'])
@login_required
def home():
    return render_template('dashboard/apps.html', user = session['user'])

@admin.route('/appLogout', methods=['GET'])
def appLogout():
    response = logoutUser()
    return response;

@admin.route('/apps/create', methods=['GET'])
@login_required
def app_create():
    return render_template('dashboard/app_create.html', user = session['user'])

@admin.route('/apps', methods=['GET', 'POST'])
@login_required
def apps():
    if request.method == 'POST':
        return AppController.store(request)
    
    return AppController.index()

@admin.route('/apps/<app_id>', methods=['GET', 'POST'])
@login_required
def get_or_update_app(app_id):
    if request.method == 'GET':
        return AppController.find(app_id)
    return AppController.update(request, app_id)

@admin.route('/apps/<app_id>/edit', methods=['GET'])
@login_required
def edit_app(app_id):
    return AppController.edit_page(app_id)

@admin.route('/apps/<app_id>/delete', methods=['GET'])
@login_required
def delete(app_id):
    return AppController.delete_app(app_id)

@admin.route('/api/apps/<app_id>/feeds', methods=['GET'])
@login_required
def get_app_feeds(app_id):
    return respondWithCollection(AppController.get_app_feeds(app_id))
    
