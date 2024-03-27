from django.http import JsonResponse
from django.conf import settings
from oauth2.views import oauth2_get_token
from urllib.request import Request, urlopen
import json

def get_user_data(access_token):
	user_request = Request("https://api.intra.42.fr/v2/me", headers={"Authorization": f"Bearer {access_token}"})
	user_response = urlopen(user_request)
	user_data = user_response.read().decode("utf-8")
	return json.loads(user_data)

def intra42_login(request):
	access_token = oauth2_get_token(request)
	user_data = get_user_data(access_token)
	return JsonResponse(user_data, safe=False)
