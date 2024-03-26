from django.shortcuts import render
from oauth2.views import oauth2_request_code, oauth2_get_token
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse

def login_intra(request):
    
	return HttpResponse("Hello, world. You're at the user index.")
