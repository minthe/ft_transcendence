from django.conf import settings
from django.http import JsonResponse
from .models import User
from ft_jwt.ft_jwt.ft_jwt import FT_JWT

jwt = FT_JWT(settings.JWT_SECRET)

def checkValueExists(key, value):
	try:
		user = User.objects.get(**{key: value})
		return True
	except User.DoesNotExist:
		return False

def returnUserId(username):
	user = User.objects.get(username=username)
	if user:
		return user.user_id
	else:
		return 0

def check_password(username, password):
	user = User.objects.get(username=username)
	if user.check_password(password):
		return True
	else:
		return False

def createIntraUser(user_data):
	for data_key in user_data.keys():
		if data_key not in user_data:
			raise Exception('Missing data')
	user = User()
	user.intra_id = user_data['intra_id']
	user.username = user_data['username']
	if checkValueExists('alias', user_data['username']):
		user.alias = f"{user_data['username']} the second"
	else:
		user.alias = user_data['username']
	user.email = user_data['email']
	user.avatar = user_data['image']
	user.set_password('')
	user.second_factor_enabled = False
	max_id = User.get_highest_user_id()
	if max_id and max_id >= 2:
		user.user_id = max_id + 1
	else:
		user.user_id = 2
	user.save()

def createUser(data):
	for data_key in data.keys():
		if data_key not in data:
			raise Exception('Missing data')
	user = User()
	user.username = data['username']
	if checkValueExists('alias', data['username']):
		user.alias = f"{data['username']} the second"
	else:
		user.alias = data['username']
	user.email = data['email']
	user.set_password(data['password'])
	user.second_factor_enabled = False
	user.avatar = f"https://api.dicebear.com/8.x/{settings.AVATAR_STYLE}/svg?seed={data['username']}"
	max_id = User.get_highest_user_id()
	if max_id and max_id >= 2:
		user.user_id = max_id + 1
	else:
		user.user_id = 2
	user.save()
	return user

def updateValue(user_id, key, value):
	user = User.objects.get(user_id=user_id)
	setattr(user, key, value)
	user.save()

def getValue(user_id, key):
	try: # TODO valentin: refactor error handling (remove try catch in child and dont return JsonResponse in child, use second_factor as reference)
		user = User.objects.get(user_id=user_id)
		value = getattr(user, key, None)
		return value
	except User.DoesNotExist:
		return JsonResponse({'message': 'User not found'}, status=404)
	except AttributeError:
		return JsonResponse({'message': f'Attribute "{key}" not found for the user'}, status=400)
	except Exception as e:
		error_message = str(e)
		if settings.DEBUG == "True":
			print(f"An error occurred: {error_message}")
		return JsonResponse({'message': 'An error occurred while retrieving the value'}, status=500)

