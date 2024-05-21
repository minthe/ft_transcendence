from django.conf import settings
from django.core.mail import send_mail
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

def send_welcome_email(username, email_to):
    email_from = settings.EMAIL_HOST_USER
    login_url = f'https://{settings.CURRENT_HOST}'

    email_subject = 'Welcome to PlayPong'
    email_body = f'Hi {username},\n\nYou can log in to our platform at: {login_url}'
    send_mail(
        email_subject,
        email_body,
        email_from,
        [email_to],
        fail_silently=False,
    )

def send_verification_email(username, code, email_to):
    email_from = settings.EMAIL_HOST_USER
    email_subject = 'PlayPong - Your 2FA Code'
    email_body = f'Hi {username},\n\nYour 2fa code is: {code}\n\nThe code is valid for 5 minutes.'
    send_mail(
        email_subject,
        email_body,
        email_from,
        [email_to],
        fail_silently=False,
    )
    if settings.DEBUG == "True":
        print(f'2FA code sent to {email_to}')

def validator(email):
	email_validator = EmailValidator(message='Email invalid')
	try:
		email_validator(email)
		return True
	except ValidationError as e:
		return False