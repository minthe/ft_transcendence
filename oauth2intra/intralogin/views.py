from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
import os
import requests

auth_url_intra = os.environ['AUTH_URL_INTRA']

def home(request: HttpRequest) -> JsonResponse:
	return JsonResponse({ "msg": "Hello World!" })

def intra_login(request: HttpRequest):
	return redirect(auth_url_intra)

def intra_login_redirect(request: HttpRequest):
	code = request.GET.get('code')
	exchange_code(code)
	print(code)
	return JsonResponse({ "msg": "Redirected." })

def exchange_code(code: str):
	data = {
		"client_id": os.environ.get('CLIENT_ID'),
		"client_secret": os.environ.get('CLIENT_SECRET'),
		"grant_type": "authorization_code",
		"code": code,
		"redirect_uri": os.environ.get('REDIRECT_URI'),
		"scope": "public"
	}
	headers = {
		"Content-Type": 'application/x-www-form-urlencoded'
	}
	oauth_url = os.environ.get('OAUTH_URL')
	response = requests.post(oauth_url, data=data, headers=headers)
	if response.text:
		credentials = response.json()
	else:
		print("Empty response received")
		credentials = None
	print(response)
	credentials = response.json()
	print(credentials)
	print(data)