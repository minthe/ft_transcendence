import json
from django.conf import settings
from django.http import JsonResponse
from urllib.request import Request, urlopen
from user import views as user_views
from ft_jwt.ft_jwt.ft_jwt import FT_JWT

jwt = FT_JWT(settings.JWT_SECRET)

@jwt.token_required
def profile(request):
	'''
	This function is used to get or update the profile infos of a user
	API Endpoint: /user/profile
	'''
	try:
		user_id = request.user_id
		if not user_views.checkValueExists('user_id', user_id):
			return JsonResponse({'message': 'User not found'}, status=404)

		if request.method == 'PUT':
			# TODO valentin input validation
			data = json.loads(request.body.decode('utf-8'))
			email = data.get('email')
			alias = data.get('alias')

			if user_views.getValue(user_id, 'email') != email and user_views.checkValueExists('email', email):
				return JsonResponse({'message': "Email already taken"}, status=409)
			if user_views.getValue(user_id, 'alias') != alias and user_views.checkValueExists('alias', alias):
				return JsonResponse({'message': "Alias already taken"}, status=409)
			if user_views.getValue(user_id, 'alias') != alias and user_views.checkValueExists('username', alias):
				return JsonResponse({'message': "Alias cannot be set to a existing username"}, status=409)

			# Request an GAME_CHAT service
			jwt_token = jwt.createToken(user_id)
			game_chat_headers = {
				"Content-Type": 'application/json',
				"Cookie": f"jwt_token={jwt_token}; HttpOnly"
			}
			game_chat_data = {
				'alias': alias,
			}
			game_chat_request_url = f"{settings.MS_GAME_CHAT}/game/user/alias"
			encoded_data = json.dumps(game_chat_data).encode("utf-8")
			print(f"request_to_game_chat url: {game_chat_request_url}")
			game_chat_request = Request(game_chat_request_url, method='PUT', data=encoded_data, headers=game_chat_headers)
			game_chat_response = urlopen(game_chat_request)
			if game_chat_response.getcode() == 200:
				user_views.updateValue(user_id, 'alias', alias)
				user_views.updateValue(user_id, 'email', email)
				return JsonResponse({'message': 'Profile updated successfully'}, status=200)
			elif game_chat_response.getcode() == 409:
				return JsonResponse({'message': 'updating Profile failed'}, status=409)
			else:
				return JsonResponse({'message': '[game_chat] Internal server error'}, status=500)

		elif request.method == 'GET':
			avatar = user_views.getValue(user_id, 'avatar')
			email = user_views.getValue(user_id, 'email')
			alias = user_views.getValue(user_id, 'alias')
			return JsonResponse({
				'avatar': avatar,
				'email': email,
				'alias': alias,
				}, status=200)
		else:
			return JsonResponse({'message': 'Method not allowed'}, status=405)

	except Exception as e:
		error_message = str(e)
		print(f"An error occurred: {error_message}")
		return JsonResponse({'message': error_message}, status=500)
