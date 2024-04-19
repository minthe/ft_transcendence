from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from ft_jwt.ft_jwt.ft_jwt import FT_JWT

jwt = FT_JWT(settings.JWT_SECRET)

@jwt.token_required
@require_http_methods(["GET"])
def heartbeat(request):
	'''
	This function is used to check if the service is up and running
	API Endpoint: /user/heartbeat
	'''
	try:
		return JsonResponse({'message': "Service is up and running"}, status=200)
	except Exception as e:
		error_message = str(e)
		print(f"An error occurred: {error_message}")
		return JsonResponse({'message': error_message}, status=503)