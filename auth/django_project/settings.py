from pathlib import Path
import os

CURRENT_HOST = os.environ.get('CURRENT_HOST')

DJANGO_SECRET = os.environ.get('DJANGO_SECRET')

POSTGRES_ENGINE = os.environ.get('POSTGRES_ENGINE')
POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST = 'users_db'
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')

REDIRECT_URI = os.environ.get('REDIRECT_URI')
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
OAUTH_URL = os.environ.get('OAUTH_URL')

ALLOWED_HOSTS = [CURRENT_HOST]

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = DJANGO_SECRET

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True # TODO minthe change to False

AUTHENTICATION_BACKENDS = [
    'intralogin.auth.IntraAuthenticationBackend'
]

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
	"intralogin.apps.IntraloginConfig",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
]

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