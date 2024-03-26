from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.conf import settings
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from jwt.views import generate_jwt
import json

redirect_uri = f"https://{settings.CURRENT_HOST}{settings.REDIRECT_URI}"

# request authorization code
def oauth2_request_code(request):
	data = {
		"client_id": settings.CLIENT_ID,
		"redirect_uri": redirect_uri,
		"response_type": "code"
	}
	return redirect(f"{settings.OAUTH_AUTH}?{urlencode(data)}")

# get access_token
def oauth2_get_token(request):
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


	# generate jwt
	# jwt_token = generate_jwt(credentials)
 
	# # add user
	# new_user = User(intra='vfuhlenb', jwt_token=jwt_token)
	# new_user.save()
 
	# all_users = User.objects.all()

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