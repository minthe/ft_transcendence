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
REDIRECT_URI = read_secret_from_vault('REDIRECT_URI')
CLIENT_ID = read_secret_from_vault('CLIENT_ID')
CLIENT_SECRET = read_secret_from_vault('CLIENT_SECRET')
OAUTH_AUTH = os.environ.get('OAUTH_AUTH')
OAUTH_TOKEN = os.environ.get('OAUTH_TOKEN')
# email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.office365.com'  # Outlook SMTP server
EMAIL_PORT = 587  # Outlook SMTP port
EMAIL_USE_TLS = True  # Use TLS for security
EMAIL_HOST_USER = read_secret_from_vault('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = read_secret_from_vault('EMAIL_HOST_PASSWORD')

ALLOWED_HOSTS = ['*']

BASE_DIR = Path(__file__).resolve().parent.parent

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