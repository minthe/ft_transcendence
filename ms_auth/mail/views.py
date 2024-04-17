from django.conf import settings
from django.core.mail import send_mail
from ft_jwt.ft_jwt.ft_jwt import FT_JWT

jwt = FT_JWT(settings.JWT_SECRET)

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
