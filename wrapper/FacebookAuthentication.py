from env import FACEBOOK_APP_ID, FACEBOOK_APP_SECRET
import oauth2 as oauth
import urlparse
import json
from Auth import helpers

def facebookDefaults():
	default = {}
	default['token_request_uri'] = "https://www.facebook.com/dialog/oauth"
	default['user_redirect_uri'] = helpers.getHostFromEnv()+"/user/login/facebook/authcallback"
	default['login_failed_url'] = '/user/login/facebook'
	default['access_token_uri'] = 'https://graph.facebook.com/oauth/access_token?'
	return default

# To Redirect the user for facebook login
def redirectTo():
	url = "{token_request_uri}?client_id={client_id}&app_id={app_id}&redirect_uri={redirect_uri}".format(
		token_request_uri = facebookDefaults()['token_request_uri'],
		client_id = FACEBOOK_APP_ID,
		app_id = FACEBOOK_APP_ID,
		redirect_uri = facebookDefaults()['user_redirect_uri'],
		)
	return redirect(url)

# To Authorize the user with facebook signin
def authorize(request):
	if 'code' not in request.GET:
		return False
	consumer = oauth.Consumer(key=FACEBOOK_APP_ID, secret=FACEBOOK_APP_SECRET)
	client = oauth.Client(consumer)
	request_url = facebookDefaults()['access_token_uri'] + 'client_id=%s&redirect_uri=%s&client_secret=%s&code=%s' % (FACEBOOK_APP_ID, facebookDefaults()['user_redirect_uri'], FACEBOOK_APP_SECRET, request.GET['code']) 
	resp, content = client.request(request_url, 'GET')
	access_token = json.loads(content)['access_token']
	# access_token = dict(urlparse.parse_qsl(content))['access_token']
	request_url = 'https://graph.facebook.com/me?access_token=%s&fields=id,name,email,picture' % access_token
	resp, content = client.request(request_url, 'GET')
	print content
	return content