from django.conf import settings
from django.http import HttpResponse, JsonResponse
from intra42.views import intra42_getUserData
from oauth2.views import oauth2_getToken
from users.views import users_checkIntraUserExists, users_createIntraUser, users_returnSubFromIntraId
from ft_jwt.ft_jwt.ft_jwt import FT_JWT

jwt = FT_JWT(settings.JWT_SECRET)

def authManager_logout(request):
	"""
	View for logging out a user.
	"""
	jwt_token = request.COOKIES.get('jwt_token')

	if jwt_token is not None:
		response = JsonResponse({'success': True, 'message': 'Logged out successfully'})
		response.delete_cookie('jwt_token')
		status_code = 200
	else:
		response = JsonResponse({'success': False, 'message': 'No token to delete'})
		status_code = 404

	response.status_code = status_code
	return response

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