from pathlib import Path
import os

ALLOWED_HOSTS = [os.environ.get('CURRENT_HOST')]

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET')

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
        'ENGINE': os.environ.get('POSTGRES_ENGINE'),
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'users_db',
        'PORT': os.environ.get('POSTGRES_PORT')
    }
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "CET"
USE_I18N = True
USE_TZ = True