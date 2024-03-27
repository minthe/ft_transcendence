import hashlib, base64, hmac, json
from django.conf import settings
from datetime import datetime, timedelta
from datetime import timedelta
from django.http import HttpResponse

def jwt_createToken(sub):
	"""
	takes a json object and returns a JWT token
	- token contains user_id and expiration date (1 day)
	"""
	# create header and payload
	current_time = datetime.utcnow()
	expire_time = current_time + timedelta(days=1)
	expire_timestamp = int(expire_time.timestamp())

	header = {
		'alg': 'HS256',
		'typ': 'JWT'}
	payload = {
		'sub': sub,
		'exp': expire_timestamp
	}

	# encode header and payload with base64
	encoded_header = base64.urlsafe_b64encode(json.dumps(header).encode('utf-8')).rstrip(b'=').decode('utf-8')
	encoded_payload = base64.urlsafe_b64encode(json.dumps(payload).encode('utf-8')).rstrip(b'=').decode('utf-8')
	# create signature with header and payload
	signature = hmac.new(settings.SECRET_KEY.encode('utf-8'), f'{encoded_header}.{encoded_payload}'.encode('utf-8'), hashlib.sha256).digest()
	# encode signature with base64
	encoded_signature = base64.urlsafe_b64encode(signature).rstrip(b'=').decode('utf-8')
	# create JWT token
	token = f'{encoded_header}.{encoded_payload}.{encoded_signature}'
	print ("create token: " + token)
	return token

def jwt_validateToken(token):
	"""
	takes a JWT token and returns True if the token is valid
    """
	# Split token into its components
	encoded_header, encoded_payload, encoded_signature = token.split('.')

	header = json.loads(base64.urlsafe_b64decode(encoded_header + '=' * (4 - len(encoded_header) % 4)))
	payload = json.loads(base64.urlsafe_b64decode(encoded_payload + '=' * (4 - len(encoded_payload) % 4)))
	signature = base64.urlsafe_b64decode(encoded_signature + '=' * (4 - len(encoded_signature) % 4))

	expected_signature = hmac.new(settings.SECRET_KEY.encode('utf-8'), f'{encoded_header}.{encoded_payload}'.encode('utf-8'), hashlib.sha256).digest()
	if not hmac.compare_digest(signature, expected_signature):
		return False, "Signature mismatch"

	# Check if the token is expired
	if 'exp' in payload:
		expiration_time = datetime.utcfromtimestamp(payload['exp'])
		if expiration_time < datetime.now():
			return False, "Token expired"
	else:
		return False, "Expiration time not found in payload"

	# Token is valid
	return True, "Token is valid"

def jwt_getUserId(token):
	"""
	takes a JWT token and returns the user_id
	"""
	encoded_header, encoded_payload, encoded_signature = token.split('.')
	payload = json.loads(base64.urlsafe_b64decode(encoded_payload + '=' * (4 - len(encoded_payload) % 4)))
	user_id = payload['sub']
	return user_id
