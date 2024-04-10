from django.conf import settings
from django.http import HttpResponse, JsonResponse
from intra42 import views as intra42_views
from oauth2 import views as oauth2_views
from user import views as user_views
from ft_jwt.ft_jwt.ft_jwt import FT_JWT

jwt = FT_JWT(settings.JWT_SECRET)

def checkTokenExist(request):
	jwt_token = request.COOKIES.get('jwt_token')

	if jwt_token is not None:
		response = JsonResponse({'success': True, 'message': 'Token exists'})
		status_code = 200
	else:
		response = JsonResponse({'success': False, 'message': 'Token does not exists'})
		status_code = 404

	response.status_code = status_code
	return response

def logout(request):
	"""
	View for logging out a user.
	"""
	jwt_token = request.COOKIES.get('jwt_token')

	if jwt_token is not None:
		response = JsonResponse({'success': True, 'message': 'Logged out successfully'})
		response.delete_cookie('jwt_token')
		status_code = 200
	else:
		response = JsonResponse({'success': False, 'message': 'No token to delete'})
		status_code = 404

	response.status_code = status_code
	return response

def login(request):
    if request.method == 'POST':
        # Get the username and password from the request
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Log the received payload
        print(f"Received payload: username={username}, password={password}")

        # You can add your login logic here and return the appropriate response

        # For debugging, return the received payload as a JSON response
        return JsonResponse({'username': username, 'password': password}, status=200)

    # Handle other HTTP methods as needed
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def loginIntra(request):
	"""
	- get user data from 42intra
	- check if user exists in database
	- if not, create user
	- generate/refresh JWT token
	"""
	# get user data from 42intra
	access_token = oauth2_views.getToken(request)
	user_data = intra42_views.getUserData(access_token)

	# check if user exists in database
	if not user_views.checkIntraUserExists(user_data['intra_id']):
		user_views.createIntraUser(user_data)

	userId = user_views.returnUserId(user_data['intra_id'])
	jwt_token = jwt.createToken(userId)

	if not jwt.validateToken(jwt_token):
		response = JsonResponse({'success': False, 'message': 'Login failed'})
		response.status_code = 401
		return response

	response = JsonResponse({'success': True, 'message': 'Logged in successfully'})
	response.status_code = 200
	response.set_cookie('jwt_token', jwt_token, httponly=True)
	return response