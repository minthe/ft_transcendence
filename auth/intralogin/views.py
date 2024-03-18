import json
from django.conf					import settings
from django.shortcuts				import render, redirect
from django.http					import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth			import authenticate, login
from django.contrib.auth.decorators	import login_required
from urllib.parse					import urlencode
from urllib.request					import Request, urlopen

@login_required(login_url='/auth/login')
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
	current_host = settings.CURRENT_HOST
	redirect_uri = settings.REDIRECT_URI
	if redirect_uri:
		redirect_uri = f"https://{current_host}{redirect_uri}"
	client_id = settings.CLIENT_ID
	redirect_uri = redirect_uri
	authorization_url = f"https://api.intra.42.fr/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
	print("Authorization URL:", authorization_url) 
	return redirect(authorization_url)

def intra_login_redirect(request: HttpRequest):
	code = request.GET.get('code')
	print("Code:", code)
	user = exchange_code(code)
 
	intra_user = authenticate(request, user=user)
	print("Intra_user:", intra_user)
 
	if intra_user is not None:
		login(request, intra_user)
		return redirect("/auth/user")
	else:
		return HttpResponse("Authentication Failed")

def exchange_code(code: str):
    current_host = settings.CURRENT_HOST
    redirect_uri = settings.REDIRECT_URI
    if redirect_uri:
        redirect_uri = f"https://{current_host}{redirect_uri}"
    data = {
        "grant_type": "authorization_code",
        "client_id": settings.CLIENT_ID,
        "client_secret": settings.CLIENT_SECRET,
        "code": code,
        "redirect_uri": redirect_uri,
        "scope": "public"
    }
    data_encoded = urlencode(data).encode("utf-8")
    headers = {
        "Content-Type": 'application/x-www-form-urlencoded'
    }
    authorization_url = settings.OAUTH_URL
    
    request = Request(authorization_url, data=data_encoded, headers=headers)
    response = urlopen(request)
    response_data = response.read().decode("utf-8")
    
    print("exchange response:", response_data)
    credentials = json.loads(response_data)
    print("exchange credentials:", credentials)
    
    access_token = credentials['access_token']
    user_request = Request("https://api.intra.42.fr/v2/me")
    user_request.add_header("Authorization", f"Bearer {access_token}")
    user_response = urlopen(user_request)
    user_data = user_response.read().decode("utf-8")
    
    print("user response:", user_data)
    
    user = json.loads(user_data)
    return user
