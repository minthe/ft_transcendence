"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
import hvac
from pathlib import Path

def read_secret_from_vault(key):
    # Construct the secret path using the key
    secret_path = f"secret/data/{key}"
    
    # Initialize the Vault client
    vault_client = hvac.Client(url='http://vault:8200', token='root')

    # Read the secret from Vault
    response = vault_client.read(secret_path)

    # Check if the read operation was successful
    if response and response.get('data') and response['data'].get('data'):
        # Extract and return the secret data
        secret_data = response['data']['data']
        # Return the value corresponding to the given key
        return secret_data.get(key)
    else:
        print(f"Failed to read secret from Vault at '{secret_path}'")
        return None

JWT_SECRET = read_secret_from_vault('JWT_SECRET')

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.office365.com'  # Outlook SMTP server
# EMAIL_PORT = 587  # Outlook SMTP port
# EMAIL_USE_TLS = True  # Use TLS for security
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

AVATAR_STYLE_BOT = os.environ.get('AVATAR_STYLE_BOT')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = read_secret_from_vault('DJANGO_SECRET')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG')
# -> prints (sensitive) data to the console, should not be readable by others

APPEND_SLASH = False

ALLOWED_HOSTS = [os.environ.get('CURRENT_HOST'), 'backend', 'localhost', '172.16.10.7']

# Application definition
INSTALLED_APPS = [
    'daphne',  # HAS to be on top
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'backend_app',
    ]


# those are applied to all requests:
MIDDLEWARE = [

    'backend_app.middleware.cors.CorsMiddleware',  # custom middleware to enable cors policy
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]


# path to the urls.py file [all my endpoints]:
ROOT_URLCONF = 'backend.urls'

# before this:
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'], # html pages to render / my folder in parent backend folder
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

ASGI_APPLICATION = 'backend.asgi.application'

current_host = os.environ.get('CURRENT_HOST')
if current_host:
    current_host = 'https://' +  current_host
    CSRF_TRUSTED_ORIGINS = [current_host]
else:
    CSRF_TRUSTED_ORIGINS = []

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('POSTGRES_ENGINE'),
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'game_chat_db',
        'PORT': os.environ.get('POSTGRES_PORT')
    }
}

# comes from 'django.contrib.auth' Application:
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'game/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
