import json
from django.conf import settings
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.utils.crypto import get_random_string
from django.views.decorators.http import require_http_methods
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from django.shortcuts import redirect
from user import views as user_views
from second_factor import views as second_factor_views
from mail import views as mail_views
from oauth2 import views as oauth2_views
from intra42 import views as intra42_views
from . import serializers as serializers_views
from ft_jwt.ft_jwt.ft_jwt import FT_JWT

jwt = FT_JWT(settings.JWT_SECRET)

def store_secret(id, secret, prefix):
	cache.set(f'{prefix}_{id}', secret, 300)

def get_secret(id, prefix):
	return cache.get(f'{prefix}_{id}')

@require_http_methods(["POST"])
def register(request):
	'''
	This function is used to register a new user
	API Endpoint: /user/register
	'''
	try:
		with transaction.atomic():
			data =json.loads(request.body)
			username = data.get('username')
			email = data.get('email')
			password = data.get('password')
			try:
				serializers_views.validate_username(username)
				if settings.STRONG_PASSWORD == "True":
					serializers_views.validate_password(password)
			except ValidationError as e:
				return JsonResponse({'message': str(e)}, status=400)
			except Exception as e:
				return JsonResponse({'message': str(e)}, status=400)

			if mail_views.validator(email) == False:
				return JsonResponse({'message': 'Email invalid'}, status=400)

			if user_views.checkValueExists('username', username):
				return JsonResponse({'message': "Username already taken"}, status=409)
			
			if user_views.checkValueExists('email', email):
				return JsonResponse({'message': "Email already taken"}, status=409)

			user = user_views.createUser(data)
			user_id = user_views.returnUserId(username)
			avatar = user_views.getValue(user_id, 'avatar')
			username = user_views.getValue(user_id, 'username')
			second_factor_status = user_views.getValue(user_id, 'second_factor_enabled')
			jwt_token = jwt.createToken(user_id)

			# request to game-chat
			game_chat_headers = {
				"Content-Type": 'application/json',
				"Cookie": f"jwt_token={jwt_token}; HttpOnly"
			}
			game_chat_data = {
				'username': username,
				'avatar': avatar,
			}
			game_chat_request_url = f"{settings.MS_GAME_CHAT}/game/user"
			encoded_data = json.dumps(game_chat_data).encode("utf-8")

			print(f"request_to_game_chat url: {game_chat_request_url}")
			game_chat_request = Request(game_chat_request_url, method='POST', data=encoded_data, headers=game_chat_headers)
			game_chat_response = urlopen(game_chat_request)
			if game_chat_response.getcode() == 200:
				response = {
					'user_id': user_id,
					'username': username,
					'second_factor': second_factor_status
				}
				json_response = json.dumps(response)
				response = HttpResponse(json_response, content_type='application/json', status=200)
				response.set_cookie('jwt_token', jwt_token, httponly=True)
				if settings.WELCOME_MAIL == "True":
					mail_views.send_welcome_email(username, user_views.getValue(user_id, 'email'))
				return response
			elif game_chat_response.getcode() == 409:
				return JsonResponse({'message': "user already exists"}, status=409)
			else:
				return JsonResponse({'message': "Failed to create user in game chat"}, status=500)
	except Exception as e:
		error_message = str(e)
		if settings.DEBUG == "True":
			print(f"An error occurred in api_register: {error_message}")
		return JsonResponse({'message': error_message}, status=500)

@require_http_methods(["POST", "GET"])
def login(request):
	'''
	This function is used to log in a user
	API Endpoint: /user/login
	'''
	try:
		intra_status = 200
		if request.method == "POST":
			data =json.loads(request.body)
			username = data.get('username')
			password = data.get('password')

			try:
				serializers_views.validate_username(username)
				if settings.STRONG_PASSWORD == "True":
					serializers_views.validate_password(password)
			except ValidationError as e:
				return JsonResponse({'message': str(e)}, status=409)

			if not user_views.checkValueExists('username', username):
				return JsonResponse({'message': "User not found"}, status=404)
			if not user_views.check_password(username, password):
				return JsonResponse({'message': "Credentials are wrong"}, status=409)

			user_id = user_views.returnUserId(username)
	
			#2fa
			if user_views.getValue(user_id, 'second_factor_enabled') == True:
				second_factor_views.create_2fa(user_id)
				return JsonResponse({'user_id': user_id, 'second_factor': True}, status=401)

			second_factor_status = user_views.getValue(user_id, 'second_factor_enabled')
			jwt_token = jwt.createToken(user_id)
			response = JsonResponse({'user_id': user_id, 'username': username, 'second_factor': second_factor_status})
			response.set_cookie('jwt_token', jwt_token, httponly=True)
			response.status_code = 200
			return response
		elif request.method == "GET":
			jwt_token = request.COOKIES.get('jwt_token')
			id_cookie = request.COOKIES.get('id')
			intra_status = get_secret(id_cookie, 'intra_status')
			if settings.DEBUG == "True":
				print (intra_status)
				print (id_cookie)
			if jwt_token and jwt.validateToken(jwt_token):
				user_id = jwt.getUserId(jwt_token)
				username = user_views.getValue(user_id, 'username')

				#2fa
				if user_views.getValue(user_id, 'second_factor_enabled') == True:
					second_factor_views.create_2fa(user_id)
					return JsonResponse({'user_id': user_id, 'username': username, 'second_factor': True}, status=401)

				second_factor_status = user_views.getValue(user_id, 'second_factor_enabled')
				response = JsonResponse({'user_id': user_id, 'username': username, 'second_factor': second_factor_status})
				jwt_token = jwt.createToken(user_id)
				response.set_cookie('jwt_token', jwt_token, httponly=True)
				response.status_code = 200
				return response
			elif id_cookie  and jwt_token is None:
				secret = get_secret(id_cookie, 'oauth2_token')
				user_data = intra42_views.getUserData(secret)
				user_id = user_views.returnUserId(user_data['username'])
				if not user_views.checkValueExists('user_id', user_id):
					return JsonResponse({'message': 'User not found'}, status=404)
				username = user_views.getValue(user_id, 'username')
				#2fa
				if user_views.getValue(user_id, 'second_factor_enabled') == True:
					second_factor_views.create_2fa(user_id)
					return JsonResponse({'user_id': user_id, 'username': username, 'second_factor': True}, status=401)

				second_factor_status = user_views.getValue(user_id, 'second_factor_enabled')
				response = JsonResponse({'user_id': user_id, 'username': username, 'second_factor': second_factor_status})
				jwt_token = jwt.createToken(user_id)
				response.set_cookie('jwt_token', jwt_token, httponly=True)
				response.status_code = 200
				return response
			else:
				if intra_status == 400:
					return JsonResponse({'message': '42Intra currently out of service'}, status=400)
				return JsonResponse({'message': 'Unauthorized'}, status=401)
	except Exception as e:
		error_message = str(e)
		if settings.DEBUG == "True":
			print(f"An error occurred in api_login: {error_message}")
		if intra_status == 400:
			return JsonResponse({'message': '42Intra currently out of service'}, status=400)
		return JsonResponse({'message': error_message}, status=500)

@require_http_methods(["POST"])
def logout(request):
	'''
	This function is used to log out a user
	API Endpoint: /user/logout
	'''
	try:
		jwt_token = request.COOKIES.get('jwt_token')

		if jwt_token is not None:
			response = JsonResponse({'message': 'Logged out successfully'})
			response.delete_cookie('jwt_token')
			status_code = 200
		else:
			response = JsonResponse({'message': 'User was not logged in'})
			status_code = 200

		response.status_code = status_code
		return response
	except Exception as e:
		error_message = str(e)
		if settings.DEBUG == "True":
			print(f"An error occurred in api_logout: {error_message}")
		return JsonResponse({'message': error_message}, status=500)

# ----------- OAUTH2 -----------

# request authorization code
def oauth2_login(request):
	'''
	This function is used to request an authorization code
	API Endpoint: user/oauth2/login
	'''
	try:
		data = {
			"client_id": settings.CLIENT_ID,
			"redirect_uri": settings.REDIRECT_URI,
			"scope": settings.INTRA_SCOPE,
			"state": settings.INTRA_STATE,
			"response_type": "code"
		}
		return redirect(f"{settings.OAUTH_AUTH}?{urlencode(data)}")
	except Exception as e:
		error_message = str(e)
		if settings.DEBUG == "True":
			print(f"An error occurred in api_oauth2_login: {error_message}")
		return JsonResponse({'message': error_message}, status=500)

def oauth2_redirect(request):
	try:
		with transaction.atomic():
			id_hash = get_random_string(length=12)
			if request.GET.get('state') != settings.INTRA_STATE:
				return JsonResponse({'message': 'Unauthorized (state does not match)'}, status=401)

			access_token = oauth2_views.getToken(request)


			user_data = intra42_views.getUserData(access_token)

			if settings.GET_INTRA_USERS_LIST == "True" and user_data['username'] == "vfuhlenb":
				intra42_views.getIntraUsersList(access_token)

			if not user_views.checkValueExists('intra_id', user_data['intra_id']):

				if settings.WELCOME_MAIL == "True":
					mail_views.send_welcome_email(user_data['username'], user_data['email'])
				user_views.createIntraUser(user_data)


				user_id = user_views.returnUserId(user_data['username'])
				jwt_token = jwt.createToken(user_id)

				# request to game-chat
				username = user_views.getValue(user_id, 'username')
				avatar = user_views.getValue(user_id, 'avatar')
				game_chat_headers = {
					"Content-Type": 'application/json',
					"Cookie": f"jwt_token={jwt_token}; HttpOnly"
				}
				game_chat_data = {
					'username': username,
					'avatar': avatar,
				}
				game_chat_request_url = f"{settings.MS_GAME_CHAT}/game/user"
				encoded_data = json.dumps(game_chat_data).encode("utf-8")

				# print(f"request_to_game_chat url: {game_chat_request_url}")
				game_chat_request = Request(game_chat_request_url, method='POST', data=encoded_data, headers=game_chat_headers)
				game_chat_response = urlopen(game_chat_request)
				if game_chat_response.getcode() == 200:
					response = HttpResponse(status=200)
					response.set_cookie('id',id_hash, httponly=True, expires=300)
					response.set_cookie('jwt_token', jwt_token, httponly=True)
					return response
				elif game_chat_response.getcode() == 409:
					return JsonResponse({'message': "user already exists"}, status=409)
				else:
					return JsonResponse({'message': "Failed to create user in game chat"}, status=500)

			user_id = user_views.returnUserId(user_data['username'])
			username = user_views.getValue(user_id, 'username')

			#2fa
			if user_views.getValue(user_id, 'second_factor_enabled') == True:
				store_secret(id_hash, access_token, 'oauth2_token')
				print (f"token: {access_token}")
				# second_factor_views.create_2fa(user_id)
				response = HttpResponse(status=200)
				response.set_cookie('id',id_hash, httponly=True, expires=300)
				return response

			jwt_token = jwt.createToken(user_id)

			response = HttpResponse(status=200)
			response.set_cookie('id',id_hash, httponly=True, expires=300)
			response.set_cookie('jwt_token', jwt_token, httponly=True)
			return response
	except Exception as e:
		error_message = str(e)
		if settings.DEBUG == "True":
			print(f"An error occurred in api_oauth2_redirect: {error_message}")
		store_secret(id_hash, 400, 'intra_status')
		response = HttpResponse(status=400)
		response.set_cookie('id',id_hash, httponly=True, expires=300)
		return response
