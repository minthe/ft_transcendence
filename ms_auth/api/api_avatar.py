import json, base64, os
from django.conf import settings
from django.http import JsonResponse
from urllib.request import Request, urlopen
from user import views as user_views
from ft_jwt.ft_jwt.ft_jwt import FT_JWT

jwt = FT_JWT(settings.JWT_SECRET)

@jwt.token_required
def avatar(request):
	'''
	This function is used to get or update the avatar of a user
	API Endpoint: /user/avatar
	'''
	try:
		user_id = request.user_id
		if not user_views.checkValueExists('user_id', user_id):
			return JsonResponse({'message': 'User not found'}, status=404)

		if request.method == 'PUT':
			request_body = json.loads(request.body)
			avatar_binary = request_body.get('avatar') # TODO valentin check if data is valid and if size over 5mb handle error

			if avatar_binary:
				missing_padding = len(avatar_binary) % 4
				if missing_padding != 0:
					avatar_binary += '=' * (4 - missing_padding)
				format, imgstr = avatar_binary.split(';base64,')
				ext = format.split('/')[-1]

				filename = f"{user_views.getValue(user_id, 'username')}.{ext}"
				
				save_folder = f"{settings.LOC_AVATAR}/{user_views.getValue(user_id, 'id')}/"
				if not os.path.exists(save_folder):
					os.makedirs(save_folder)

				with open(os.path.join(save_folder, filename), "wb") as f:
					f.write(base64.b64decode(imgstr))

				user_views.updateValue(user_id, 'avatar', os.path.join(save_folder, filename))

				# Request an GAME_CHAT service
				avatar = user_views.getValue(user_id, 'avatar') # TODO valentin update with new avatar
				jwt_token = jwt.createToken(user_id)
				game_chat_headers = {
					"Content-Type": 'application/json',
					"Cookie": f"jwt_token={jwt_token}; HttpOnly"
				}
				game_chat_data = {
					'avatar': avatar,
				}
				game_chat_request_url = f"{settings.MS_GAME_CHAT}/game/user/avatar"
				encoded_data = json.dumps(game_chat_data).encode("utf-8")
				print(f"request_to_game_chat url: {game_chat_request_url}")
				game_chat_request = Request(game_chat_request_url, method='PUT', data=encoded_data, headers=game_chat_headers)
				game_chat_response = urlopen(game_chat_request)
				if game_chat_response.getcode() == 200:
					user_views.updateValue(user_id, 'avatar', avatar)
					return JsonResponse({'message': 'Avatar updated successfully'}, status=200)
				elif game_chat_response.getcode() == 409:
					return JsonResponse({'message': 'updating value failed'}, status=409)
				else:
					return JsonResponse({'message': '[game_chat] Internal server error'}, status=500)
			else:
				return JsonResponse({'message': 'avatar is required'}, status=400)

		if request.method == 'GET': # TODO valentin change later to url that points to the avatar stored as file
			avatar = user_views.getValue(user_id, 'avatar')
			if avatar:
				return JsonResponse({'avatar': avatar}, status=200)
			else:
				return JsonResponse({'message': 'Avatar not found'}, status=404)
		else:
			return JsonResponse({'message': 'Method not allowed'}, status=405)

	except Exception as e:
		error_message = str(e)
		print(f"An error occurred: {error_message}")
		return JsonResponse({'message': error_message}, status=500)
