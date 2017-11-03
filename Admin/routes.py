from flask import Flask, Blueprint, request, session
from flask import render_template, jsonify
from App.Response import *
from Controllers.AuthController import *
from Controllers import AppController
from decorators import api_login_required, login_required

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/')
def index():
    return render_template('admin_login.html')

@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    user = legacyLoginApi(data)
    return respondWithItem(user, 200)

@auth.route('/appLogin', methods=['POST'])
def app_login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = legacyLogin(email, password)
    return user

@auth.route('/google', methods=['POST'])
def google():
    response = googleLogin()
    

@auth.route('/home', methods=['GET'])
@login_required
def home():
    return render_template('dashboard/apps.html', user = session['user'])

@auth.route('/logout', methods=['GET'])
@api_login_required
def api_logout():
    token = request.headers['access-token']
    response = logout(token)
    return respondOk('Successfully Logout');

@auth.route('/appLogout', methods=['GET'])
def appLogout():
    response = logoutUser()
    return response;

@auth.route('/apps/create', methods=['GET'])
@login_required
def app_create():
    return render_template('dashboard/app_create.html', user = session['user'])

@auth.route('/apps', methods=['GET', 'POST'])
@login_required
def apps():
    if request.method == 'POST':
        return AppController.store(request)
    
    return AppController.index()

@auth.route('/apps/<app_id>', methods=['GET', 'POST'])
@login_required
def get_or_update_app(app_id):
    if request.method == 'GET':
        return AppController.find(app_id)
    return AppController.update(request, app_id)

@auth.route('/apps/<app_id>/edit', methods=['GET'])
@login_required
def edit_app(app_id):
    return AppController.edit_page(app_id)

@auth.route('/apps/<app_id>/delete', methods=['GET'])
@login_required
def delete(app_id):
    return AppController.delete_app(app_id)

@auth.route('/api/apps/<app_id>/feeds', methods=['GET'])
@login_required
def get_app_feeds(app_id):
    print respondWithCollection(AppController.get_app_feeds(app_id))
    return respondWithCollection(AppController.get_app_feeds(app_id))
    
