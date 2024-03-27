import json
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from intra42.views import intra42_getUserData
from oauth2.views import oauth2_getToken
from jwt.views import jwt_createToken, jwt_validateToken, jwt_getUserId
from users.views import users_checkIntraUserExists

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
	if users_checkIntraUserExists(user_data['intra_id']):
		# if user exists, return JWT token
		# token = jwt_createToken(user_data)
		return HttpResponse("user exists in database")
	else:
		# if user does not exist, create user
		# create user
		# return JWT token
		pass
	# if not, create user

	# generate/refresh JWT token

	# is_valid, message = jwt_validateToken(token)
	# print("jwt_getUserId:", jwt_getUserId(token))

	return HttpResponse("user does not exists in database")
	# return HttpResponse(message)