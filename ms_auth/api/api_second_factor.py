import json
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from user import views as user_views
from second_factor import views as second_factor_views
from ft_jwt.ft_jwt.ft_jwt import FT_JWT

jwt = FT_JWT(settings.JWT_SECRET)

@require_http_methods(["POST"])
def second_factor_verify(request):
	# TODO valentin: Input Validation
	data = json.loads(request.body.decode('utf-8'))
	user_id = data.get('user_id')
	code = data.get('code')

	if not user_views.checkUserExists('user_id', user_id):
		return HttpResponse(status=404)

	is_verified, error_message = second_factor_views.verify_2fa(user_id, code)
	if is_verified:
		response = HttpResponse(status=200)
		response.set_cookie('jwt_token', jwt.createToken(user_id), httponly=True)
		return response
	else:
		return JsonResponse({'message': error_message}, status=401)

def second_factor(request):
	try:
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
	except Exception as e:
		error_message = str(e)
		print(f"An error occurred: {error_message}")
		return JsonResponse({'message': error_message}, status=500)

@require_http_methods(["POST"])
@jwt.token_required
def second_factor_generate(request):
	user_id = request.user_id
	if not user_views.checkUserExists('user_id', user_id):
		return HttpResponse(status=404)
	second_factor_views.create_2fa(request.user_id)
	return HttpResponse(status=200)

@require_http_methods(["GET"])
@jwt.token_required
def second_factor_status(request):
	if not user_views.checkUserExists('user_id', request.user_id):
		return HttpResponse(status=404)
	second_factor_status = user_views.getValue(request.user_id, 'second_factor_enabled')
	return JsonResponse({'second_factor': second_factor_status}, status=200)

@require_http_methods(["PUT"])
@jwt.token_required
def second_factor_activate(request):
	# TODO valentin: Input Validation
	data = json.loads(request.body.decode('utf-8'))
	code = data.get('code')
	user_id = request.user_id
	if not user_views.checkUserExists('user_id', user_id):
		return HttpResponse(status=404)
	if user_views.getValue(request.user_id, 'second_factor_enabled') == True:
		return HttpResponse(status=409)
	is_verified, error_message = second_factor_views.verify_2fa(user_id, code)
	if is_verified:
		user_views.updateValue(request.user_id, 'second_factor_enabled', True)
		response = HttpResponse(status=200)
		response.set_cookie('jwt_token', jwt.createToken(user_id), httponly=True)
		return response
	else:
		return JsonResponse({'message': error_message}, status=401)

@require_http_methods(["DELETE"])
@jwt.token_required
def second_factor_deactivate(request):
	# TODO valentin: Input Validation
	data = json.loads(request.body.decode('utf-8'))
	code = data.get('code')
	user_id = request.user_id
	if not user_views.checkUserExists('user_id', user_id):
		return HttpResponse(status=404)
	if user_views.getValue(request.user_id, 'second_factor_enabled') == False:
		return HttpResponse(status=409)
	is_verified, error_message = second_factor_views.verify_2fa(user_id, code)
	if is_verified:
		user_views.updateValue(request.user_id, 'second_factor_enabled', False)
		response = HttpResponse(status=200)
		response.delete_cookie('jwt_token')
		return response
	else:
		return JsonResponse({'message': error_message}, status=401)
