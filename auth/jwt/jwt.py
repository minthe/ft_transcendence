import hashlib, base64, hmac, json
from datetime import datetime, timedelta
from django.http import HttpResponse

class JWT:

	def __init__(self, secret):
		self.secret = secret

	def base64url_encode(self, input):
		return base64.urlsafe_b64encode(input).decode('utf-8').rstrip('=')

	def createToken(self, sub):
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
		json_header = json.dumps(header, separators=(",",":")).encode()
		json_payload = json.dumps(payload, separators=(",",":")).encode()
		# encode header and payload with base64
		encoded_header = self.base64url_encode(json_header)
		encoded_payload = self.base64url_encode(json_payload)
		# create signature with header and payload
		signature = hmac.new(self.secret.encode('utf-8'), f'{encoded_header}.{encoded_payload}'.encode('utf-8'), hashlib.sha256).digest()
		# encode signature with base64
		encoded_signature = self.base64url_encode(signature)
		# create JWT token
		token = f'{encoded_header}.{encoded_payload}.{encoded_signature}'
		print (token)
		return token

	def validateToken(self, token):
		"""
		takes a JWT token and returns True if the token is valid
		"""
		# Split token into its components
		encoded_header, encoded_payload, encoded_signature = token.split('.')

		header = json.loads(base64.urlsafe_b64decode(encoded_header + '=' * (4 - len(encoded_header) % 4)))
		payload = json.loads(base64.urlsafe_b64decode(encoded_payload + '=' * (4 - len(encoded_payload) % 4)))
		signature = base64.urlsafe_b64decode(encoded_signature + '=' * (4 - len(encoded_signature) % 4))

		expected_signature = hmac.new(self.secret.encode('utf-8'), f'{encoded_header}.{encoded_payload}'.encode('utf-8'), hashlib.sha256).digest()
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
