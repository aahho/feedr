from flask import Flask, Blueprint, request, session
from flask import render_template, jsonify
from App.Response import *
from Controllers.AuthController import *
from decorators import api_login_required

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/users/register', methods=['POST'])
def register():
    data = request.json
    user = create_user(data)
    return respondWithItem(user, statusCode=201)

@auth.route('/users/login', methods=['POST'])
def login():
    data = request.json
    user = legacy_login_api(data)
    return respondWithItem(user, statusCode=200)

@auth.route('/users/google', methods=['GET'])
def google():
    token = request.args.get('token')
    response = googleLogin(token)
    return respondWithItem(response, statusCode=200)
    
@auth.route('/users/logout', methods=['GET'])
@api_login_required
def api_logout():
    token = request.headers['access-token']
    response = logout(token)
    return respondOk('Successfully Logout');