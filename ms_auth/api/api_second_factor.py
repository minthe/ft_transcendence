import json
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from user import views as user_views
from second_factor import views as second_factor_views
from . import serializers as serializers_views
from ft_jwt.ft_jwt.ft_jwt import FT_JWT

jwt = FT_JWT(settings.JWT_SECRET)

@require_http_methods(["POST"])
def second_factor_verify(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		user_id = data.get('user_id')
		code = data.get('code')

		try:
			serializers_views.validate_2fa_code(code)
			serializers_views.validate_user_id(user_id)
		except ValidationError as e:
			return JsonResponse({'message': str(e)}, status=409)

		if not user_views.checkValueExists('user_id', user_id):
			return HttpResponse(status=404)

		if not user_views.getValue(user_id, 'second_factor_enabled'):
			return JsonResponse({'message': '2FA not enabled'}, status=409)

		is_verified, error_message = second_factor_views.verify_2fa(user_id, code)
		if is_verified:
			response = HttpResponse(status=200)
			response.set_cookie('jwt_token', jwt.createToken(user_id), httponly=True)
			return response
		else:
			return JsonResponse({'message': error_message}, status=401)
	except Exception as e:
		error_message = str(e)
		if settings.DEBUG == "True":
			print(f"An error occurred verifying 2fa: {error_message}")
		return JsonResponse({'message': error_message}, status=500)

def second_factor(request):
	if request.method == 'POST':
		return second_factor_generate(request)
	elif request.method == 'GET':
		return second_factor_status(request)
	elif request.method == 'PUT':
		return second_factor_activate(request)
	elif request.method == 'DELETE':
		return second_factor_deactivate(request)
	else:
		return HttpResponse(status=405)

@require_http_methods(["POST"])
@jwt.token_required
def second_factor_generate(request):
	try:
		user_id = request.user_id
		if not user_views.checkValueExists('user_id', user_id):
			return HttpResponse(status=404)
		second_factor_views.create_2fa(request.user_id)
		return HttpResponse(status=200)
	except Exception as e:
		error_message = str(e)
		if settings.DEBUG == "True":
			print(f"An error occurred generating the 2fa code: {error_message}")
		return JsonResponse({'message': error_message}, status=500)

@require_http_methods(["GET"])
@jwt.token_required
def second_factor_status(request):
	try:
		if not user_views.checkValueExists('user_id', request.user_id):
			return HttpResponse(status=404)
		second_factor_status = user_views.getValue(request.user_id, 'second_factor_enabled')
		return JsonResponse({'second_factor': second_factor_status}, status=200)
	except Exception as e:
		error_message = str(e)
		if settings.DEBUG == "True":
			print(f"An error occurred getting 2fa status: {error_message}")
		return JsonResponse({'message': error_message}, status=500)

@require_http_methods(["PUT"])
@jwt.token_required
def second_factor_activate(request):
	data = json.loads(request.body.decode('utf-8'))
	code = data.get('code')
	try:
		serializers_views.validate_2fa_code(code)
	except ValidationError as e:
		return JsonResponse({'message': str(e)}, status=409)
	try:
		user_id = request.user_id
		if not user_views.checkValueExists('user_id', user_id):
			return HttpResponse(status=404)
		is_verified, error_message = second_factor_views.verify_2fa(user_id, code)
		if is_verified:
			user_views.updateValue(user_id, 'second_factor_enabled', True)
			return HttpResponse(status=200)
		else:
			return JsonResponse({'message': error_message}, status=401)
	except Exception as e:
		error_message = str(e)
		if settings.DEBUG == "True":
			print(f"An error occurred activating 2fa: {error_message}")
		return JsonResponse({'message': error_message}, status=500)

@require_http_methods(["DELETE"])
@jwt.token_required
def second_factor_deactivate(request):
	data = json.loads(request.body.decode('utf-8'))
	code = data.get('code')
	try:
		serializers_views.validate_2fa_code(code)
	except ValidationError as e:
		return JsonResponse({'message': str(e)}, status=409)
	try:
		user_id = request.user_id
		if not user_views.checkValueExists('user_id', user_id):
			return HttpResponse(status=404)
		is_verified, error_message = second_factor_views.verify_2fa(user_id, code)
		if is_verified:
			user_views.updateValue(user_id, 'second_factor_enabled', False)
			return HttpResponse(status=200)
		else:
			return JsonResponse({'message': error_message}, status=401)
	except Exception as e:
		error_message = str(e)
		if settings.DEBUG == "True":
			print(f"An error occurred deactivating 2fa: {error_message}")
		return JsonResponse({'message': error_message}, status=500)
