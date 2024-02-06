from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
import os
import requests

# auth_url_intra = os.environ['AUTH_URL_INTRA']

def home(request: HttpRequest) -> JsonResponse:
	return JsonResponse({ "msg": "Hello World!" })

def intra_login(request: HttpRequest):
	return redirect(os.environ['AUTH_URL_INTRA'])

def intra_login_redirect(request: HttpRequest):
	code = request.GET.get('code')
	print(code)
	user = exchange_code(code)
	authenticate(request, user=user)
	return JsonResponse({ "user": user })

def exchange_code(code: str):
	data = {
		"grant_type": "authorization_code",
		"client_id": os.environ.get('CLIENT_ID'),
		"client_secret": os.environ.get('CLIENT_SECRET'),
		"code": code,
		"redirect_uri": os.environ.get('REDIRECT_URI'),
		"scope": "public"
	}
	headers = {
		"Content-Type": 'application/x-www-form-urlencoded'
	}
	response = requests.post("https://api.intra.42.fr/oauth/token", data=data, headers=headers)
	print(response)
	credentials = response.json()
	print(credentials)
	access_token = credentials['access_token']
	response = requests.get("https://api.intra.42.fr/v2/me", headers={
		"Authorization": 'Bearer %s' % access_token})
	print(response)
	user = response.json()
	# print(user)
	return user