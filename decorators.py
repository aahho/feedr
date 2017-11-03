from flask import Flask, session, redirect, request
from Exceptions.ExceptionHandler import FeedrException
from Admin.AuthRepository import UserTokenRepository
from models import UserToken

def login_required(func):
	def wraps(*args, **kwargs):
		if session.has_key('token'):
			repo = UserTokenRepository()
			tokenObj = repo.check_valid_token(UserToken, session['token'])
			if hasattr(tokenObj, 'token'):
			 	return func(*args, **kwargs)
		return redirect('/admin/')
	wraps.func_name = func.func_name
	return wraps

def api_login_required(func):
	def wraps(*args, **kwargs):
		if request.headers.has_key('access-token'):
			repo = UserTokenRepository()
			token = request.headers['access-token']
			tokenObj = repo.check_valid_token(UserToken, token)
			if hasattr(tokenObj, 'token'):
			 	return func(*args, **kwargs)
		raise FeedrException('Unauthorized request', 401)
	wraps.func_name = func.func_name
	return wraps