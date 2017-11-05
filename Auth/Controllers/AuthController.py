from flask import Flask, render_template, redirect, flash, url_for, session
from models import User, UserToken, UserDetail
from Exceptions.ExceptionHandler import FeedrException
from Auth.AuthRepository import AuthRepository, UserTokenRepository, UserDetailsRepository
import helpers, datetime
from Auth.AuthValidator import create_user_rule
from wrapper import GoogleAuthentication

def create_user(data):
	create_user_rule(data)
	repo = AuthRepository()
	user_detail_repo = UserDetailsRepository()
	inputs = {
		'id' : helpers.generate_unique_code().__str__(),
		'email' : data['email'],
		'password' : helpers.hash_password(data['password']), 
		'display_name' : data['displayName'],
		'is_password_change_required' : data['is_password_change_required']\
			if 'is_password_change_required' in data else False
	}
	user = repo.store(User, inputs)
	user_detail = {
		'user_id' : user.id,
		'first_name' : data['firstName']\
			if 'firstName' in data else None,
		'last_name' : data['lastName']\
			if 'lastName' in data else None
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
	# GoogleAuthentication.authenticate_token(token)
	user_info = GoogleAuthentication.get_user_details(token)
	repo = AuthRepository().filter_attribute(user_info['email'])
	if repo is None:
		data = {
			'email' : user_info['email'],
			'password' : None,
			'displayName' : user_info['display_name'],
			'firstName' : user_info['first_name'],
			'last_Name' : user_info['last_name'],
			'is_password_change_required' : user_info['is_password_change_required']
		}
		create_user(data)
	user_token = helpers.access_token()
	return tokenRepo.store(UserToken, 
		{
		'token' : user_token, 
		'user_id' : userObj.id
		})
	# return user_info
	# social = GoogleSocialAuthentication()
 	#return social.redirect('user')

def logout(token):
	tokenRepo = UserTokenRepository()
	return tokenRepo.deleteToken(UserToken, token)

