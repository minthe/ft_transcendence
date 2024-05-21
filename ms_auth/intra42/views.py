import json, http.client
from django.conf import settings
from urllib.request import Request, urlopen

def getUserData(access_token):
	user_headers = {
		'Authorization': f'Bearer {access_token}',
		'Content-type': 'application/json'
	}
	conn = http.client.HTTPSConnection('api.intra.42.fr')
	conn.request('GET', '/v2/me', headers=user_headers)
	data_response_raw = conn.getresponse()
	print("getUserData data_response_raw.status:", data_response_raw.status)
	if data_response_raw.status == 200:
		data_response = json.loads(data_response_raw.read().decode('utf-8'))
		# remove unnecessary data
		cleaned_user_data = {
		"intra_id": data_response["id"],
		"username": data_response["login"],
		"email": data_response["email"],
		"first_name": data_response["first_name"],
		"last_name": data_response["last_name"],
		"image": data_response["image"]["versions"]["medium"],
	}
		return cleaned_user_data
	else:
		return None

def getIntraUsersList(access_token):
	if settings.DEBUG == "True":
		print("getIntraUsersList")
	user_request = Request("https://api.intra.42.fr/v2/users?campus_id=wolfsburg&range[pool_year]=2021,2024&range[updated_at]=2024-05-01T00:00:00.000Z,22024-06-01T00:00:00.000Z&sort=-last_seen_at&page=1", headers = {"Authorization": f"Bearer {access_token}"})
	user_response = urlopen(user_request)
	user_data = user_response.read().decode("utf-8")
	users_list = json.loads(user_data)

	# Retrieve custom headers
	x_page = user_response.headers.get('X-Page')
	x_per_page = user_response.headers.get('X-Per-Page')
	x_total = user_response.headers.get('X-Total')
	if settings.DEBUG == "True":
		print("X-Page:", x_page)
		print("X-Per-Page:", x_per_page)
		print("X-Total:", x_total)

	return users_list