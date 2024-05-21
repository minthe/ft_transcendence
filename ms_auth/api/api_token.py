from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from ft_jwt.ft_jwt.ft_jwt import FT_JWT

jwt = FT_JWT(settings.JWT_SECRET)

@jwt.token_required
@require_http_methods(["GET"])
def token_existence(request):
	'''
	This function is used to check if a token exists
	API Endpoint: /user/token-existence
	'''
	try:
		jwt_token = request.COOKIES.get('jwt_token')

		if jwt_token is not None:
			return JsonResponse({'message': "Token exists"}, status=200)
		else:
			return JsonResponse({'message': "Token does not exist"}, status=404)
	except Exception as e:
		error_message = str(e)
		if settings.DEBUG == "True":
			print(f"An error occurred in api_token_existence: {error_message}")
		return JsonResponse({'message': error_message}, status=500)
	
@jwt.token_required
def token(request):
	try:
		jwt_token = request.COOKIES.get('jwt_token')

		if jwt_token is not None:
			if request.method == 'GET':
				return JsonResponse({'message': "not implemented yet"}, status=200) # TODO valentin implement
			else:
				return HttpResponse(status=405)
		else:
			return JsonResponse({'message': "Token does not exist"}, status=404)
	except Exception as e:
		error_message = str(e)
		if settings.DEBUG == "True":
			print(f"An error occurred in api_token: {error_message}")
		return JsonResponse({'message': error_message}, status=500)
