import json
from django.conf import settings
from django.http import JsonResponse
from urllib.request import Request, urlopen

def intra42_cleanUserData(user_data):
	"""
	cleans user profile data from 42intra
	- returns cleaned user data as json
	"""
	user_data_dict = json.loads(user_data)
	cleaned_user_data = {
		"id": user_data_dict["id"],
		"login": user_data_dict["login"],
		"email": user_data_dict["email"],
		"first_name": user_data_dict["first_name"],
		"last_name": user_data_dict["last_name"],
		"image": user_data_dict["image"]["versions"]["medium"],
	}
	return cleaned_user_data

def intra42_getUserData(access_token):
	"""
	returns whole user profile data from 42intra as json
 	- from api endpoint: /v2/me
	"""
	user_request = Request("https://api.intra.42.fr/v2/me", headers={"Authorization": f"Bearer {access_token}"})
	user_response = urlopen(user_request)
	user_data = user_response.read().decode("utf-8")
	# remove unnecessary data
	cleaned_user_data = intra42_cleanUserData(user_data)
	return cleaned_user_data
