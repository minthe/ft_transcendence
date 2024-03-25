import json
from intralogin.models	import User
from django.http		import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts	import redirect
from django.conf		import settings
from urllib.parse		import urlencode
from urllib.request		import Request, urlopen
from urllib.error		import HTTPError

def oauth_login(request):
    # request authorization code
	redirect_uri = f"https://{settings.CURRENT_HOST}{settings.REDIRECT_URI}"
	authorization_url = f"https://api.intra.42.fr/oauth/authorize?client_id={settings.CLIENT_ID}&redirect_uri={redirect_uri}&response_type=code"
	print("Authorization URL:", authorization_url) 
	return redirect(authorization_url)

def oauth_authenticate(request):
	# get access_token
	data = {
		"grant_type": "authorization_code",
		"client_id": settings.CLIENT_ID,
		"client_secret": settings.CLIENT_SECRET,
		"code": request.GET.get("code"),
		"redirect_uri": f"https://{settings.CURRENT_HOST}{settings.REDIRECT_URI}",
		"scope": "public"
	}
	headers = {
		"Content-Type": 'application/x-www-form-urlencoded'
	}
	request = Request(settings.OAUTH_URL, data=urlencode(data).encode("utf-8"), headers=headers)

	try:
		response = urlopen(request)
		response_data = response.read().decode("utf-8")
		credentials = json.loads(response_data)
  
		# add user
		
  
		return JsonResponse(credentials)
	except HTTPError as e:
		if e.code == 401:
			redirect_url = '/oauth/login'
		else:
			redirect_url = '/'
		return redirect(redirect_url)

