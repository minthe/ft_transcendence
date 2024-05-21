import json, http.client
from django.conf import settings
from django.http import JsonResponse

# get access_token
def getToken(request):
	try:
		data = json.dumps({
			'client_id': settings.CLIENT_ID,
			'client_secret': settings.CLIENT_SECRET,
			'redirect_uri': settings.REDIRECT_URI,
			'code': request.GET.get("code"),
			'grant_type': 'authorization_code'
		})
		headers = {
			'Content-Type': 'application/json'
		}
		conn = http.client.HTTPSConnection('api.intra.42.fr')
		conn.request('POST', '/oauth/token', data, headers)

		response_raw = conn.getresponse()
		response = json.loads(response_raw.read().decode('utf-8'))

		access_token = response.get("access_token")

		return (access_token)
	except Exception as e:
		error_message = str(e)
		if settings.DEBUG == "True":
			print(f"An error occurred: {error_message}")
		return JsonResponse({'message': error_message}, status=500)