from flask import Flask, Blueprint, request, session
from flask import render_template
from App.Response import *
from Controllers.AuthController import *
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
	return render_template('home.html', user = session['user'])

@auth.route('/logout', methods=['GET'])
@api_login_required
def api_logout():
	token = request.headers['access-token']
	response = logout(token)
	return respondOk('Successfully Logout');

@auth.route('/appLogout', methods=['GET'])
@api_login_required
def appLogout():
	response = logoutUser()
	return response;