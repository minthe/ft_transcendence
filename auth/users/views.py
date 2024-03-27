from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password

def index(request):
	return HttpResponse("Hello, world. You're at the user index.")
