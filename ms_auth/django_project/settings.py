import os, logging
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
    
CURRENT_HOST = os.environ.get('CURRENT_HOST')
DJANGO_SECRET = read_secret_from_vault('DJANGO_SECRET')
JWT_SECRET = read_secret_from_vault('JWT_SECRET')
POSTGRES_ENGINE = os.environ.get('POSTGRES_ENGINE')
POSTGRES_DB = read_secret_from_vault('POSTGRES_DB')
POSTGRES_USER = read_secret_from_vault('POSTGRES_USER')
POSTGRES_PASSWORD = read_secret_from_vault('POSTGRES_PASSWORD')
POSTGRES_HOST = 'users_db'
POSTGRES_PORT = read_secret_from_vault('POSTGRES_PORT')
CLIENT_ID = read_secret_from_vault('CLIENT_ID')
CLIENT_SECRET = read_secret_from_vault('CLIENT_SECRET')
OAUTH_AUTH = os.environ.get('OAUTH_AUTH')
OAUTH_TOKEN = os.environ.get('OAUTH_TOKEN')

MS_GAME_CHAT = read_secret_from_vault('MS_GAME_CHAT')

# network
LOC_AVATAR = os.environ.get('LOC_AVATAR')
AVATAR_DEFAULT = os.environ.get('AVATAR_DEFAULT')
AVATAR_STYLE = os.environ.get('AVATAR_STYLE')
# email settings
REDIRECT_URI = f"https://{CURRENT_HOST}{os.environ.get('REDIRECT_URI')}"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.office365.com'  # Outlook SMTP server
EMAIL_PORT = 587  # Outlook SMTP port
EMAIL_USE_TLS = True  # Use TLSfor security
EMAIL_HOST_USER = read_secret_from_vault('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = read_secret_from_vault('EMAIL_HOST_PASSWORD')

INTRA_STATE = read_secret_from_vault('INTRA_STATE')
INTRA_SCOPE = os.environ.get('INTRA_SCOPE')

INTRA_SCOPE='public'

WELCOME_MAIL = os.environ.get('WELCOME_MAIL')
GET_INTRA_USERS_LIST = os.environ.get('GET_INTRA_USERS_LIST')
STRONG_PASSWORD = os.environ.get('STRONG_PASSWORD')

ALLOWED_HOSTS = ['*']

BASE_DIR = Path(__file__).resolve().parent.parent

ASGI_APPLICATION = 'django_project.asgi.application'

SECRET_KEY = DJANGO_SECRET

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG')

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