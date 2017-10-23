from flask import Flask, json


def respondWithItem(data, statusCode = 200, message = 'Success', hint=''):
	response = dict(())
	response['data'] = data
	response['code'] = statusCode
	response['notification'] = {
		'seCode' : 'SE_'+str(statusCode),
		'message' : message,
		'hint' : hint,
		'type' : 'success'
	}
	response['version'] = 1
	return json.jsonify(response)

def respondOk(message = 'Success', statusCode = 200, hint=''):
	response = dict(())
	response['data'] = []
	response['code'] = statusCode
	response['notification'] = {
		'seCode' : 'SE_'+str(statusCode),
		'message' : message,
		'hint' : hint,
		'type' : 'success'
	}
	response['version'] = 1
	return json.jsonify(response)

def respondWithhError(message = 'Error', statusCode = 500, hint=''):
	response = dict(())
	response['data'] = []
	response['code'] = statusCode
	response['notification'] = {
		'seCode' : 'SE_'+str(statusCode),
		'message' : message,
		'hint' : hint,
		'type' : 'error'
	}
	response['version'] = 1
	return json.jsonify(response)