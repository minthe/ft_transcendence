import json
from django.conf import settings
from django.http import JsonResponse
from urllib.request import Request, urlopen

def intra42_getUserData(access_token):
	"""
	returns whole user profile data from 42intra as json
 	- from api endpoint: /v2/me
	"""
	user_request = Request("https://api.intra.42.fr/v2/me", headers={"Authorization": f"Bearer {access_token}"})
	user_response = urlopen(user_request)
	user_data = user_response.read().decode("utf-8")
	return json.loads(user_data)
