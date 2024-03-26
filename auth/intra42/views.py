from django.http import JsonResponse
from django.conf import settings
from oauth2.views import oauth2_get_token

def get_user_data(access_token):
	return (access_token)

def login_intra(request):
	print (request)
	return JsonResponse(oauth2_get_token(request), safe=False)
