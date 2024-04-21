import json
from django.conf import settings
from django.http import JsonResponse
from urllib.parse import urlencode
from urllib.request import Request, urlopen

# get access_token
def getToken(request):
	try:
		data = {
			"grant_type": "authorization_code",
			"client_id": settings.CLIENT_ID,
			"client_secret": settings.CLIENT_SECRET,
			"code": request.GET.get("code"),
			"redirect_uri": settings.REDIRECT_URI,
			"state": settings.INTRA_STATE,
		}
		headers = {
			"Content-Type": 'application/x-www-form-urlencoded'
		}
		request = Request(settings.OAUTH_TOKEN, data=urlencode(data).encode("utf-8"), headers=headers)

		response = urlopen(request)
		response_data = response.read().decode("utf-8")
		credentials = json.loads(response_data)

		return (credentials.get("access_token"))
	except Exception as e:
		error_message = str(e)
		print(f"An error occurred: {error_message}")
		return JsonResponse({'message': error_message}, status=500)