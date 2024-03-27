import json
from django.conf import settings
from django.http import JsonResponse
from intra42.views import intra42_getUserData
from oauth2.views import oauth2_getToken
from users.models import User

def authManager_loginIntra(request):
	"""
	- get user data from 42intra
	- check if user exists in database
	- if not, create user
	- generate/refresh JWT token
	"""
	access_token = oauth2_getToken(request)
	user_data = intra42_getUserData(access_token)
	return JsonResponse(user_data)
