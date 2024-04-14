from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from user.models import User
from user import views as user_views
from ft_jwt.ft_jwt.ft_jwt import FT_JWT

jwt = FT_JWT(settings.JWT_SECRET)

def send_verification_email(user_id, email_to):
    user = User.objects.get(user_id=user_id)
    email_from = settings.EMAIL_HOST_USER
    code = user.generate_verification_code()
    email_subject = 'PlayPong - verification code'
    email_body = f'Hi {user.username},\n\nHere your 2fa code: {code}'
    send_mail(
        'Your 2FA Code',
        f'Your 2FA code is: {code}',
        email_from,
        [email_to],
        fail_silently=False,
    )

def send_welcome_email(user_id, email_to):
    user = User.objects.get(user_id=user_id)
    email_from = settings.EMAIL_HOST_USER
    login_url = f'https://{settings.CURRENT_HOST}'

    email_subject = 'Welcome to PlayPong'
    email_body = f'Hi {user.username},\n\nYou can log in to our platform at: {login_url}'

    try:
        send_mail(
            email_subject,
            email_body,
            email_from,
            [email_to],
            fail_silently=False,
        )
    except Exception as e:
        print(f'Error sending welcome email: {e}')
        return JsonResponse({'message': 'Failed sending welcome Email'}, status=500)

@jwt.token_required
def verify_two_factor_code(request, user_id, code, username):
	try:
		if not user_views.checkUserExists('username', username):
			return JsonResponse({'message': "User not found"}, status=404)
		user = User.objects.get(username=username)
		if user.verify_verification_code(code):
			return JsonResponse({'message': "Sucessfully verified"}, status=200)
		else:
			return JsonResponse({'message': 'Invalid or expired verification code'}, status=400)
	except Exception as e:
		print("in verify two_factor_code: ", e)
		return JsonResponse({'message': 'Validation failed'}, status=500)