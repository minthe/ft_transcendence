from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import os
import requests

@login_required(login_url='/oauth2/login')
def get_authenticated_user(request: HttpRequest):
	print(request.user)
	user = request.user
	return JsonResponse({
		"id": user.id,
		"login": user.login,
		"email": user.email,
		"first_name": user.first_name,
		"last_name": user.last_name,
		"last_login": user.last_login,
		"session age": request.session.get_expiry_age(),
	 })

def intra_login(request: HttpRequest):
	current_host = os.environ['CURRENT_HOST']
	redirect_uri = os.environ.get('REDIRECT_URI')
	if redirect_uri:
		redirect_uri = f"https://{current_host}{redirect_uri}"
	client_id = os.environ.get('CLIENT_ID')
	redirect_uri = redirect_uri
	authorization_url = f"https://api.intra.42.fr/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
	print("Authorization URL:", authorization_url) 
	return redirect(authorization_url)

def intra_login_redirect(request: HttpRequest):
	code = request.GET.get('code')
	print(code)
	user = exchange_code(code)
	intra_user = authenticate(request, user=user)
	intra_user = list(intra_user).pop()
	print(intra_user)
	login(request, intra_user)
	request.session.set_expiry(20)
	print(request.session.get_expiry_age())
	return redirect("/auth/user")

def exchange_code(code: str):
	current_host = os.environ['CURRENT_HOST']
	redirect_uri = os.environ.get('REDIRECT_URI')
	if redirect_uri:
			redirect_uri = f"https://{current_host}{redirect_uri}"
	data = {
		"grant_type": "authorization_code",
		"client_id": os.environ.get('CLIENT_ID'),
		"client_secret": os.environ.get('CLIENT_SECRET'),
		"code": code,
		"redirect_uri": redirect_uri,
		"scope": "public"
	}
	headers = {
		"Content-Type": 'application/x-www-form-urlencoded'
	}
	authorization_url = os.environ.get('OAUTH_URL')
	response = requests.post(authorization_url, data=data, headers=headers)
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