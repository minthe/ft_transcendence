from django.conf import settings
from urllib.parse import urlencode
from django.shortcuts import redirect
from django.http import JsonResponse

redirect_uri = f"https://{settings.CURRENT_HOST}{settings.REDIRECT_URI}"

# request authorization code
def oauth2_login(request):
	try:
		data = {
			"client_id": settings.CLIENT_ID,
			"redirect_uri": redirect_uri,
			"response_type": "code"
		}
		print(f"oauth2 login: {settings.OAUTH_AUTH}?{urlencode(data)}")
		return redirect(f"{settings.OAUTH_AUTH}?{urlencode(data)}")
	except Exception as e:
		error_message = str(e)
		print(f"An error occurred: {error_message}")
		return JsonResponse({'message': error_message}, status=500)