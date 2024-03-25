from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse

def index(request):
	return HttpResponse("Hello, world. You're at the user index.")
