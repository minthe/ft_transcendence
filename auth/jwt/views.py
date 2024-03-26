from django.http import HttpResponse
from django.conf import settings
from datetime import datetime, timedelta
import json, hashlib, base64, hmac
from datetime import timedelta

def generate_jwt(user):
	if user:
		datetime_formatted = datetime.now().isoformat()
		payload = {
			'user_id': user.id,
			'exp': (datetime.now() + timedelta(days=1)).isoformat()
		}
	header = {
		'alg': 'HS256',
		'typ': 'JWT'}
	encoded_header = base64.urlsafe_b64encode(json.dumps(header).encode('utf-8')).decode('utf-8')
	encoded_payload = base64.urlsafe_b64encode(json.dumps(payload).encode('utf-8')).decode('utf-8')
	signature = hmac.new(settings.SECRET_KEY.encode('utf-8'), f'{encoded_header}.{encoded_payload}'.encode('utf-8'), hashlib.sha256).digest()
	encoded_signature = base64.urlsafe_b64encode(signature).decode('utf-8')
	
	jwt_token = f'{encoded_header}.{encoded_payload}.{encoded_signature}'
	return jwt_token

