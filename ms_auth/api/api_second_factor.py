import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from user import views as user_views
from second_factor import views as second_factor_views
from ft_jwt.ft_jwt.ft_jwt import FT_JWT

jwt = FT_JWT(settings.JWT_SECRET)

@jwt.token_required
@require_http_methods(["PUT"])
def second_factor_update(request):
	'''
	This function is used to enable or disable 2fa
	API Endpoint: /user/2fa/update
	'''
	try:
		# TODO @valentin: Input Validation
		data = json.loads(request.body.decode('utf-8'))
		user_id = data.get('user_id')
		second_factor = data.get('second_factor')

		user_views.updateValue(user_id, 'second_factor_enabled', second_factor)
		updated_value = user_views.getValue(user_id, 'second_factor_enabled')

		if updated_value != second_factor:
			return JsonResponse({'message': 'updating value failed'}, status=409)

		print(f"second_factor: {updated_value}")
		return JsonResponse({'message': '2fa updated successfully'}, status=200)

	except Exception as e:
		error_message = str(e)
		print(f"An error occurred: {error_message}")
		return JsonResponse({'message': error_message}, status=500)

@require_http_methods(["POST"])
def second_factor_verify(request):
	'''
	This function is used to verify the 2fa code
	API Endpoint: /user/2fa/verify
	'''
	try:
		if not user_views.checkUserExists('user_id', user_id):
			return JsonResponse({'message': 'User not found'}, status=404)

		# TODO @valentin: Input Validation
		data = json.loads(request.body.decode('utf-8'))
		user_id = data.get('user_id')
		code = data.get('code')

		is_verified, error_message = second_factor_views.verify_verification_code(user_id, code)
		if is_verified:
			return JsonResponse({'message': "Successfully verified"}, status=200)
		else:
			return JsonResponse({'message': error_message}, status=401)

	except Exception as e:
		print("in verify second_factor_code: ", e)
		return JsonResponse({'message': 'Verification failed'}, status=500)