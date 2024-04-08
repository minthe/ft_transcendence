import json
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from urllib.parse import urlencode
from urllib.request import Request, urlopen

redirect_uri = f"https://{settings.CURRENT_HOST}{settings.REDIRECT_URI}"

# request authorization code
def getCode(request):
	"""
	initiates oauth2 authorization code flow
	- redirects to /user/oauth2/redirect
	"""
	data = {
		"client_id": settings.CLIENT_ID,
		"redirect_uri": redirect_uri,
		"response_type": "code"
	}
	return redirect(f"{settings.OAUTH_AUTH}?{urlencode(data)}")

# get access_token
def getToken(request):
	"""
	returns access_token from 42intra
	"""
	data = {
		"grant_type": "authorization_code",
		"client_id": settings.CLIENT_ID,
		"client_secret": settings.CLIENT_SECRET,
		"code": request.GET.get("code"),
		"redirect_uri": redirect_uri,
		"scope": "public"
	}
	headers = {
		"Content-Type": 'application/x-www-form-urlencoded'
	}
	request = Request(settings.OAUTH_TOKEN, data=urlencode(data).encode("utf-8"), headers=headers)

	response = urlopen(request)
	response_data = response.read().decode("utf-8")
	credentials = json.loads(response_data)
	return (credentials.get("access_token"))

# handling of 401 error

	# try:
	# 	response = urlopen(request)
	# 	response_data = response.read().decode("utf-8")
	# 	credentials = json.loads(response_data)
	# 	return JsonResponse(credentials)
	# except HTTPError as e:
	# 	if e.code == 401:
	# 		redirect_url = '/oauth/login'
	# 	else:
	# 		redirect_url = '/'
	# 	return redirect(redirect_url)