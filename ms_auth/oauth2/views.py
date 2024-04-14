import json
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from user import views as user_views
from intra42 import views as intra42_views
from ft_jwt.ft_jwt.ft_jwt import FT_JWT

jwt = FT_JWT(settings.JWT_SECRET)

redirect_uri = f"https://{settings.CURRENT_HOST}{settings.REDIRECT_URI}"

# get access_token
def getToken(request):
	try:
		data = {
			"grant_type": "authorization_code",
			"client_id": settings.CLIENT_ID,
			"client_secret": settings.CLIENT_SECRET,
			"code": request.GET.get("code"),
			"redirect_uri": redirect_uri,
			"scope": "public"
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

def oauth2_redirect(request):
	try:
		access_token = getToken(request)
		user_data = intra42_views.getUserData(access_token)

		if not user_views.checkUserExists('intra_id', user_data['intra_id']):
			user_views.createIntraUser(user_data)

		user_id = user_views.returnUserId(user_data['username'])
		jwt_token = jwt.createToken(user_id)

		if not jwt.validateToken(jwt_token):
			response = JsonResponse({'message': 'Login failed'})
			response.status_code = 401
			return response

		response = JsonResponse({'message': 'Logged in successfully'})
		response.status_code = 200
		response.set_cookie('jwt_token', jwt_token, httponly=True)
		return response
	except Exception as e:
		error_message = str(e)
		print(f"An error occurred: {error_message}")
		return JsonResponse({'message': error_message}, status=500)

# handling of 401 error

	# try:
	# 	response = urlopen(request)
	# 	response_data = response.read().decode("utf-8")
	# 	credentials = json.loads(response_data)
	# 	return JsonResponse(credentials)
	# except HTTPError as e:
	# 	if e.code == 401:
	# 		redirect_url = '/oauth/login'
	# 	else:
	# 		redirect_url = '/'
	# 	return redirect(redirect_url)