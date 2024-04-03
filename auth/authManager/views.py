from django.conf import settings
from django.http import HttpResponse
from intra42.views import intra42_getUserData
from oauth2.views import oauth2_getToken
from users.views import users_checkIntraUserExists, users_createIntraUser, users_returnSubFromIntraId
from jwt.jwt import JWT

jwt = JWT(settings.JWT_SECRET)

def authManager_test(request):
	"""
	- test function to check if JWT token is valid
	"""
	jwt_token = request.COOKIES.get('jwt_token')
	if jwt_token == None:
		return HttpResponse("no token")
	print (jwt_token)
	if jwt.validateToken(jwt_token) == False:
		return HttpResponse("invalid token")
	response = HttpResponse("Cookie deleted")
	response.delete_cookie('jwt_token')
	return response

def authManager_getId(request):
	jwt_token = request.COOKIES.get('jwt_token')
	if jwt_token == None:
			return HttpResponse("no token")
	user_id = jwt.getUserId(jwt_token)
	return HttpResponse(user_id)

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
	jwt_token = jwt.createToken(sub)

	response = HttpResponse("valid token")
	response.set_cookie('jwt_token', jwt_token, httponly=True)

	if not jwt.validateToken(jwt_token):
		return HttpResponse("invalid token") 
	return response