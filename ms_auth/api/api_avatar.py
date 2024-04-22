import json
from django.conf import settings
from django.http import JsonResponse
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
