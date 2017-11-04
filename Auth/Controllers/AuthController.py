from flask import Flask, render_template, redirect, flash, url_for, session
from models import User, UserToken, UserDetail
from Exceptions.ExceptionHandler import FeedrException
from Auth.AuthRepository import AuthRepository, UserTokenRepository, UserDetailsRepository
import helpers, datetime
from Auth.AuthValidator import create_user_rule

def create_user(data):
	create_user_rule(data)
	repo = AuthRepository()
	user_detail_repo = UserDetailsRepository()
	# print helpers.generate_unique_code().__str__()
	# return "ASf"
	inputs = {
		'id' : helpers.generate_unique_code().__str__(),
		'email' : data['email'],
		'password' : helpers.hash_password(data['password']),
		'display_name' : data['displayName']
	}
	user = repo.store(User, inputs)
	user_detail = {
		'user_id' : user.id
	}
	user_detail_repo.create_user_details(UserDetail, user_detail)
	return user


def legacy_login_api(data):
	repo = AuthRepository()
	tokenRepo = UserTokenRepository()
	userObj = repo.filter_attribute(User, {'email': data['email']})
	if hasattr(userObj, 'email'):
		isValid = helpers.validate_hash_password(data['password'], userObj.password)
		if isValid:
			token = helpers.access_token()
			return tokenRepo.store(UserToken, 
				{
				'token' : token, 
				'user_id' : userObj.id
				})
	raise FeedrException('Invalid credentials', 422)

def googleLogin(token):
	pass
	# social = GoogleSocialAuthentication()
 	#return social.redirect('user')

def logout(token):
	tokenRepo = UserTokenRepository()
	return tokenRepo.deleteToken(UserToken, token)

