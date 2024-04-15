from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from .models import User
from ft_jwt.ft_jwt.ft_jwt import FT_JWT

jwt = FT_JWT(settings.JWT_SECRET)

def getId(request):
	'''
	This function is used to get the user id
	API Endpoint: /user/me
	'''
	try:
		jwt_token = request.COOKIES.get('jwt_token')
		if jwt_token == None:
				return JsonResponse({'message': "Unauthorized"}, status=401)
		user_id = jwt.getUserId(jwt_token)
		return JsonResponse({'user_id': user_id}, status=200)
	except Exception as e:
		error_message = str(e)
		print(f"An error occurred: {error_message}")
		return JsonResponse({'message': error_message}, status=500)

def checkUserExists(key, value):
	try:
		user = User.objects.get(**{key: value})
		return True
	except User.DoesNotExist:
		return False

def returnUserId(key):
	try:
		user = User.objects.get(username=key)
		return user.user_id
	except User.DoesNotExist:
		return 0

def createIntraUser(user_data):
	try:
		user = User()
		user.intra_id = user_data['intra_id']
		user.username = user_data['username']
		user.email = user_data['email']
		user.image = user_data['image']
		user.set_password('') # TODO valentin: change before production
		user.two_factor_enabled = False
		user.save()
	except Exception as e:
		error_message = str(e)
		print(f"An error occurred: {error_message}")
		return JsonResponse({'message': error_message}, status=500)

def createUser(data):
	try:
		user = User()
		user.username = data['username']
		user.email = data['email']
		user.set_password(data['password'])
		user.two_factor_enabled = False
		user.save()
		return user
	except Exception as e:
		error_message = str(e)
		print(f"An error occurred: {error_message}")
		return JsonResponse({'message': error_message}, status=500)

def returnUserPassword(username):
	try:
		user = User.objects.get(username=username)
		return user.password
	except User.DoesNotExist:
		return ''

def updateValue(user_id, key, value):
	try:
		user = User.objects.get(user_id=user_id)
		setattr(user, key, value)
		user.save()
	except Exception as e:
		error_message = str(e)
		print(f"An error occurred: {error_message}")
		return JsonResponse({'message': "updating value failed"}, status=409)

def getValue(user_id, key):
    try:
        user = User.objects.get(user_id=user_id)
        value = getattr(user, key, None)
        return value
    except User.DoesNotExist:
        return JsonResponse({'message': 'User not found'}, status=404)
    except AttributeError:
        return JsonResponse({'message': f'Attribute "{key}" not found for the user'}, status=400)
    except Exception as e:
        error_message = str(e)
        print(f"An error occurred: {error_message}")
        return JsonResponse({'message': 'An error occurred while retrieving the value'}, status=500)