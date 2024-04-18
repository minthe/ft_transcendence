import json
from django.conf import settings
from django.http import JsonResponse
from urllib.request import Request, urlopen

def cleanUserData(user_data):
	try:
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
	except Exception as e:
		error_message = str(e)
		print(f"An error occurred: {error_message}")
		return JsonResponse({'message': error_message}, status=500)

def getUserData(access_token):
	try:
		user_request = Request("https://api.intra.42.fr/v2/me", headers={"Authorization": f"Bearer {access_token}"})
		user_response = urlopen(user_request)
		user_data = user_response.read().decode("utf-8")
		# remove unnecessary data
		cleaned_user_data = cleanUserData(user_data)
		return cleaned_user_data
	except Exception as e:
		error_message = str(e)
		print(f"An error occurred: {error_message}")
		return JsonResponse({'message': error_message}, status=500)
