import os
from pathlib import Path

CURRENT_HOST = os.environ.get('CURRENT_HOST')
DJANGO_SECRET = os.environ.get('DJANGO_SECRET')
JWT_SECRET = os.environ.get('JWT_SECRET')
POSTGRES_ENGINE = os.environ.get('POSTGRES_ENGINE')
POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST = 'users_db'
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
# oauth2
REDIRECT_URI = f"https://{CURRENT_HOST}{os.environ.get('REDIRECT_URI')}"
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
OAUTH_AUTH = os.environ.get('OAUTH_AUTH')
OAUTH_TOKEN = os.environ.get('OAUTH_TOKEN')
INTRA_STATE = os.environ.get('INTRA_STATE')
INTRA_SCOPE = os.environ.get('INTRA_SCOPE')
# network
MS_GAME_CHAT = os.environ.get('MS_GAME_CHAT')
# avatar
LOC_AVATAR = os.environ.get('LOC_AVATAR')
AVATAR_DEFAULT = os.environ.get('AVATAR_DEFAULT')
AVATAR_STYLE = os.environ.get('AVATAR_STYLE')
# email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.office365.com'  # Outlook SMTP server
EMAIL_PORT = 587  # Outlook SMTP port
EMAIL_USE_TLS = True  # Use TLS for security
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
# Feature Flags
WELCOME_MAIL = os.environ.get('WELCOME_MAIL')
GET_INTRA_USERS_LIST = os.environ.get('GET_INTRA_USERS_LIST')
STRONG_PASSWORD = os.environ.get('STRONG_PASSWORD')

ALLOWED_HOSTS = ['*']

BASE_DIR = Path(__file__).resolve().parent.parent

ASGI_APPLICATION = 'django_project.asgi.application'

SECRET_KEY = DJANGO_SECRET

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

INSTALLED_APPS = [
    "api",
    "user",
    "oauth2",
    "intra42",
    "ft_jwt",
    "second_factor",
    "mail",
]


MIDDLEWARE = []

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

ROOT_URLCONF = "django_project.urls"

DATABASES = {
    'default': {
        'ENGINE': POSTGRES_ENGINE,
        'NAME': POSTGRES_DB,
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': 'users_db',
        'PORT': POSTGRES_PORT
    }
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "CET"
USE_I18N = True
USE_TZ = True