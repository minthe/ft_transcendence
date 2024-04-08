from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from ft_jwt.ft_jwt.ft_jwt import FT_JWT

jwt = FT_JWT(settings.JWT_SECRET)

def getId(request):
	jwt_token = request.COOKIES.get('jwt_token')
	if jwt_token == None:
			return HttpResponse("no token")
	user_id = jwt.getUserId(jwt_token)
	return HttpResponse(user_id)

def checkIntraUserExists(intra_id):
	"""
	- check if Intra user with "intra_id" exists in database
	- return True if user exists, False if not
	"""
	try:
		user = User.objects.get(intra_id=intra_id)
		return True
	except User.DoesNotExist:
		return False

def returnSubFromIntraId(intra_id):
	try:
		user = User.objects.get(intra_id=intra_id)
		return user.sub
	except User.DoesNotExist:
		return 0

def createIntraUser(user_data):
	"""
	- create user with "user_data" in database
	- return user object
	"""
	user = User()
	user.intra_id = user_data['intra_id']
	user.username = user_data['username']
	user.email = user_data['email']
	user.image = user_data['image']
	user.set_password('test123')
	user.save()