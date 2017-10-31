from flask import Flask, request, url_for
import datetime

'''
To create url for pagination 
'''
def url_for_other_page(page):
    args = dict(request.args)
    args['page'] = page
    return url_for(request.endpoint, _external=True, **args)

'''
To hash the password
'''
def hash_password(password):
    return bcrypt.hashpw(password, bcrypt.gensalt())

'''
To hash the access-token
'''
def access_token():
    return bcrypt.hashpw(str(random.random()), bcrypt.gensalt())

'''
To validate/comapre the hash password
@param present - user's account present password
@param requested - password requested for verification
'''
def validate_hash_password(requested, present):
    return bcrypt.checkpw(str(requested), str(present))

'''
To generate unique code
uuid package
'''
def generate_unique_code():
    return uuid.uuid4()

'''
error message
'''
def error(message):
    return {
        'message' : message, 
        'tags' : 'error'
    }

'''
success message
'''
def success(message):
    return {
        'message' : message, 
        'tags' : 'success'
    }