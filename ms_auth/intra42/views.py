import json, os
from django.http import JsonResponse
from django.conf import settings
from urllib.request import Request, urlopen

def cleanUserData(user_data):
	user_data_dict = json.loads(user_data)
	cleaned_user_data = {
		"intra_id": user_data_dict["id"],
		"username": user_data_dict["login"],
		"email": user_data_dict["email"],
		"first_name": user_data_dict["first_name"],
		"last_name": user_data_dict["last_name"],
		"image": user_data_dict["image"]["versions"]["medium"],
	}
	return cleaned_user_data

def getUserData(access_token):
	user_request = Request("https://api.intra.42.fr/v2/me", headers={"Authorization": f"Bearer {access_token}"})
	user_response = urlopen(user_request)
	user_data = user_response.read().decode("utf-8")
	# remove unnecessary data
	cleaned_user_data = cleanUserData(user_data)
	return cleaned_user_data

def getIntraUsersList(access_token):
	print("getIntraUsersList")
	user_request = Request("https://api.intra.42.fr/v2/users?campus_id=wolfsburg&range[pool_year]=2021,2024&range[updated_at]=2024-05-01T00:00:00.000Z,22024-06-01T00:00:00.000Z&sort=-last_seen_at&page=1", headers = {"Authorization": f"Bearer {access_token}"})
	user_response = urlopen(user_request)
	user_data = user_response.read().decode("utf-8")
	users_list = json.loads(user_data)

	# Retrieve custom headers
	x_page = user_response.headers.get('X-Page')
	x_per_page = user_response.headers.get('X-Per-Page')
	x_total = user_response.headers.get('X-Total')
	
	print("X-Page:", x_page)
	print("X-Per-Page:", x_per_page)
	print("X-Total:", x_total)

	# print(users_list)
	return users_list