import json
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from intra42.views import intra42_getUserData
from oauth2.views import oauth2_getToken
from jwt.views import jwt_createToken, jwt_validateToken, jwt_getUserId
from users.views import users_checkIntraUserExists, users_createIntraUser, users_returnSubFromIntraId

def authManager_loginIntra(request):
	"""
	- get user data from 42intra
	- check if user exists in database
	- if not, create user
	- generate/refresh JWT token
	"""
	# get user data from 42intra
	access_token = oauth2_getToken(request)
	user_data = intra42_getUserData(access_token)

	# check if user exists in database
	if not users_checkIntraUserExists(user_data['intra_id']):
		users_createIntraUser(user_data)

	sub = users_returnSubFromIntraId(user_data['intra_id'])
	jwt_token = jwt_createToken(sub)
	return JsonResponse(jwt_token, safe=False)