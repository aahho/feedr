from flask import Flask, json
from helpers import url_for_other_page

def respondWithItem(data, transformer='transform', statusCode=200, message = 'Success', hint=''):
	response = dict(())
	response['data'] = getattr(data, transformer)()
	response['code'] = statusCode
	response['notification'] = {
		'feedCode' : 'SE_'+str(statusCode),
		'message' : message,
		'hint' : hint,
		'type' : 'success'
	}
	response['version'] = 1
	return json.jsonify(response)

def respondWithPaginatedCollection(data, transformer='transform', statusCode = 200, message = 'Success', hint=''):
	response_data = []
	response = dict(())
	for item in data.items:
		response_data.append(getattr(item, transformer)()) 
	response['data'] = response_data
	response['code'] = statusCode
	response['meta'] = {
		'pagination' : {
			'count' : data.per_page,
			'current_page' : data.page,
			'per_page' : data.per_page,
			'total' : data.total,
			'links' : {
				'prev_page' : (url_for_other_page(data.prev_num)) if (data.prev_num is not None) else None ,
				'next_page' : (url_for_other_page(data.next_num)) if (data.next_num is not None) else None
			},
			'total_page' : data.pages,
		}
	}
	response['notification'] = {
		'feedCode' : 'SE_'+str(statusCode),
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
		'feedCode' : 'SE_'+str(statusCode),
		'message' : message,
		'hint' : hint,
		'type' : 'success'
	}
	response['version'] = 1
	return json.jsonify(response)

def respondWithError(message = 'Error', statusCode = 500, hint=''):
	response = dict(())
	response['data'] = []
	response['code'] = statusCode
	response['notification'] = {
		'feedCode' : 'SE_'+str(statusCode),
		'message' : message,
		'hint' : hint,
		'type' : 'error'
	}
	response['version'] = 1
	return json.jsonify(response)