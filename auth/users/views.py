from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import User

def index(request):
	return HttpResponse("Hello, world. You're at the user index.")

def users_checkIntraUserExists(intra_id):
	"""
	- check if Intra user with "intra_id" exists in database
	- return True if user exists, False if not
	"""
	try:
		user = User.objects.get(intra_id=intra_id)
		return True
	except User.DoesNotExist:
		return False