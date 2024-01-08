from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
import requests

auth_url_intra = "https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-fb288837c73a19518006b7f714435adbb54c59be1abf9adfc2b980585fcfdb95&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Foauth2%2Flogin%2Fredirect&response_type=code"

def home(request: HttpRequest) -> JsonResponse:
	return JsonResponse({ "msg": "Hello World!" })

def intra_login(request: HttpRequest):
	return redirect(auth_url_intra)

def intra_login_redirect(request: HttpRequest):
	code = request.GET.get('code')
	print(code)
	exchange_code(code)
	return JsonResponse({ "msg": "Redirected." })

def exchange_code(code: str):
	data = {
		"client_id": "u-s4t2ud-fb288837c73a19518006b7f714435adbb54c59be1abf9adfc2b980585fcfdb95",
		"client_secret": "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",
		"grant_type": "authorization_code",
		"code": code,
		"redirect_uri": "http://localhost:8000/oauth/login/redirect",
		"scope": "public"
	}
	headers = {
		"Content-Type": 'application/x-www-form-urlencoded'
	}
	response = requests.post("https://api.intra.42.fr/oauth/authorize", data=data, headers=headers)
	print(response)
	credentials = response.json()
	print(credentials)
	print('hello test')