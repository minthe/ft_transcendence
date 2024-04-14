import json
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from django.contrib.auth.hashers import check_password
from django.views.decorators.http import require_http_methods
from user import views as user_views
from two_factor import views as two_factor_views
from ft_jwt.ft_jwt.ft_jwt import FT_JWT

jwt = FT_JWT(settings.JWT_SECRET)

@require_http_methods(["POST"])
def register(request):
	try:
		data =json.loads(request.body)
		username = data.get('username')
		password = data.get('password')
		email = data.get('email')
		avatar = 'moon-dog.jpg'

		if user_views.checkUserExists('username', username):
			return JsonResponse({'message': "username already taken"}, status=409)
		if user_views.checkUserExists('email', email):
			return JsonResponse({'message': "email already taken"}, status=409)

		user = user_views.createUser(data)
		user_id = user_views.returnUserId(username)
		jwt_token = jwt.createToken(user_id)

		# request an game-chat
		game_chat_headers = {
			"Content-Type": 'application/json',
			"Set-Cookie": f"jwt_token={jwt_token}; HttpOnly"
		}
		game_chat_data = {
			'username': username,
			'avatar': avatar,
		}
		game_chat_request_url = f"http://172.16.10.7:6969/game/user/{user_id}"
		encoded_data = json.dumps(game_chat_data).encode("utf-8")

		print(f"request_to_game_chat url: {game_chat_request_url}")
		game_chat_request = Request(game_chat_request_url, method='POST', data=encoded_data, headers=game_chat_headers)
		game_chat_response = urlopen(game_chat_request)
		if game_chat_response.getcode() == 200:
			response = {
				'user_id': user_id,
				'username': username
			}
			json_response = json.dumps(response)
			response = HttpResponse(json_response, content_type='application/json', status=200)
			response.set_cookie('jwt_token', jwt_token, httponly=True)
			two_factor_views.send_welcome_email(user_id, user_views.getValue(user_id, 'email'))
			return response
		elif game_chat_response.getcode() == 409:
			user.delete()
			return JsonResponse({'message': "user already exists"}, status=409)
		else:
			user.delete()
			return JsonResponse({'message': "Failed to create user in game chat"}, status=500)
	except Exception as e:
		error_message = str(e)
		user.delete()
		print(f"An error occurred: {error_message}")
		return JsonResponse({'message': error_message}, status=500)

@require_http_methods(["POST"])
def login(request):
	try:
		data =json.loads(request.body)
		username = data.get('username')
		password = data.get('password')

		if not user_views.checkUserExists('username', username):
			return JsonResponse({'message': "User not found"}, status=404)
		if not check_password(password, user_views.returnUserPassword(username)):
			return JsonResponse({'message': "Credentials are wrong"}, status=401)

		user_id = user_views.returnUserId(username)
  
		#2fa
		if user_views.getValue(user_id, 'two_factor_enabled'):
			two_factor_views.send_verification_email(user_id, user_views.getValue(user_id, 'email'))
			return JsonResponse({'user_id': user_id, 'second_factor': True}, status=200) # TODO: @valentin @julien review flow
  
		jwt_token = jwt.createToken(user_id)
		response = JsonResponse({'user_id': user_id, 'username': username})
		response.set_cookie('jwt_token', jwt_token, httponly=True)
		response.status_code = 200
		return response
	except Exception as e:
		error_message = str(e)
		print(f"An error occurred: {error_message}")
		return JsonResponse({'message': error_message}, status=500)

@require_http_methods(["POST"])
def logout(request):
	try:
		jwt_token = request.COOKIES.get('jwt_token')

		if jwt_token is not None:
			response = JsonResponse({'message': 'Logged out successfully'})
			response.delete_cookie('jwt_token')
			status_code = 200
		else:
			response = JsonResponse({'message': 'No token to delete'})
			status_code = 404

		response.status_code = status_code
		return response
	except Exception as e:
		error_message = str(e)
		print(f"An error occurred: {error_message}")
		return JsonResponse({'message': error_message}, status=500)

@jwt.token_required
def avatar(request, user_id):
	try:
		if not user_views.checkUserExists('user_id', user_id):
			return JsonResponse({'message': 'User not found'}, status=404)

		if request.method == 'PUT':
			data = json.loads(request.body.decode('utf-8'))
			avatar = data.get('avatar')
			user_views.updateValue(user_id, 'avatar', avatar)
			return JsonResponse({'message': 'Avatar updated successfully'}, status=200)
		elif request.method == 'GET':
			avatar = user_views.getValue(user_id, 'avatar')
			return JsonResponse({'avatar': avatar}, status=200)
		else:
			return JsonResponse({'message': 'Method not allowed'}, status=405)

	except Exception as e:
		error_message = str(e)
		print(f"An error occurred: {error_message}")
		return JsonResponse({'message': error_message}, status=500)

@jwt.token_required
@require_http_methods(["PUT"])
def second_factor(request, user_id):
	try:
		if not user_views.checkUserExists('user_id', user_id):
			return JsonResponse({'message': 'User not found'}, status=404)

		data = json.loads(request.body.decode('utf-8'))
		second_factor = data.get('second_factor')
		user_views.updateValue(user_id, 'avatar', second_factor)
		return JsonResponse({'message': '2fa updated successfully'}, status=200)

	except Exception as e:
		error_message = str(e)
		print(f"An error occurred: {error_message}")
		return JsonResponse({'message': error_message}, status=500)
