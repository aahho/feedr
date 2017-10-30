from flask import Flask, render_template, redirect, flash, url_for, session
from models import User, UserToken
from Exceptions.ExceptionHandler import FeedrException
from Auth.AuthRepository import AuthRepository, UserTokenRepository
import helpers, datetime


def legacyLogin(email, password):
	repo = AuthRepository()
	tokenRepo = UserTokenRepository()
	userObj = repo.filter_attribute(User, {'email': email, 'is_god':True})
	if hasattr(userObj, 'email'):
		isValid = helpers.validate_hash_password(password, userObj.password)
		if isValid:
			token = helpers.access_token()
			tokenObj = tokenRepo.store(UserToken, 
				{
				'token' : token, 
				'user_id' : userObj.id
				})
			session['token'] = token
			session['user'] = userObj.transform()
			return redirect('/admin/home')
	flash(helpers.error('Invalid credentials'))
	return redirect('/admin/')

def legacyLoginApi(data):
	repo = AuthRepository()
	tokenRepo = UserTokenRepository()
	userObj = repo.filter_attribute(User, {'email': data['email'], 'is_god':True})
	if hasattr(userObj, 'email'):
		isValid = helpers.validate_hash_password(data['password'], userObj.password)
		if isValid:
			token = helpers.access_token()
			tokenObj = tokenRepo.store(UserToken, 
				{
				'token' : token, 
				'user_id' : userObj.id
				})
			return tokenObj.transform()
	raise FeedrException('Invalid credentials', 422)

def googleLogin(token):
	pass
	# social = GoogleSocialAuthentication()
 	#return social.redirect('user')

def logout(token):
	tokenRepo = UserTokenRepository()
	return tokenRepo.deleteToken(UserToken, token)

def logoutUser():
	tokenRepo = UserTokenRepository()
	tokenRepo.deleteToken(UserToken, session['token'])
	session.clear()
	flash(helpers.success('Successfully Logout'))
	return redirect('/admin/')

