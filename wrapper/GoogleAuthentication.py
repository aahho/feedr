from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from Exceptions.ExceptionHandler import FeedrException
import requests, json
from app import app

# (Receive token by HTTPS POST)
# ...

def authenticate_token(token):
    return
    print app
    try:
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), app.config['GOOGLE_CLIENT_ID'])

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']
    except ValueError:
        raise FeedrException("invalid google auth token")

def get_user_details(token):
    # user_info = requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token='+token)
    headers = {
        'Authorization': 'Bearer '+token
    }
    user_info = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers=headers)
    user_info = json.loads(user_info.content)
    if 'email' not in user_info:
        raise FeedrException("invalid google auth token")
    return create_user_data(user_info)

def create_user_data(user_info):
    print user_info
    if user_info['verified_email'] is not True:
        raise FeedrException('Email is not verified')
    return {
        'email' : user_info['email'],
        'display_name' : user_info['email'].split('@')[0],
        'first_name' : user_info['name'].split(' ')[0],
        'last_name' : user_info['family_name'],
    }