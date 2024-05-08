import os
from pathlib import Path

CURRENT_HOST = os.environ.get('CURRENT_HOST')
DJANGO_SECRET = os.environ.get('DJANGO_SECRET')
JWT_SECRET = os.environ.get('JWT_SECRET')
# network
MS_GAME_CHAT = os.environ.get('MS_GAME_CHAT')
# user
LOC_AVATAR = os.environ.get('LOC_AVATAR')
AVATAR_DEFAULT = os.environ.get('AVATAR_DEFAULT')

ALLOWED_HOSTS = ['*']

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB

ASGI_APPLICATION = 'django_project.asgi.application'

SECRET_KEY = DJANGO_SECRET

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

INSTALLED_APPS = [
    "api",
]

MIDDLEWARE = []

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

ROOT_URLCONF = "django_project.urls"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "CET"
USE_I18N = True
USE_TZ = True