import hashlib, base64, hmac, json
from datetime import datetime, timedelta
from django.http import HttpResponse

class JWT:

	def __init__(self, secret):
		self.secret = secret
		self.secret = 'gw3-3#-fGe-f3f#K_03kf2-3kf)#F_K)JF_)#fpeokwffewk30fsKPFGf'

	def base64url_encode(self, input):
		return base64.urlsafe_b64encode(input).decode('utf-8').rstrip('=')

	def createToken(self, sub):
		"""
		takes a json object and returns a JWT token
		- token contains user_id and expiration date (1 day)
		"""
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
		encoded_header = self.base64url_encode(json_header)
		encoded_payload = self.base64url_encode(json_payload)

		signature = hmac.new(self.secret.encode('utf-8'), f'{encoded_header}.{encoded_payload}'.encode('utf-8'), hashlib.sha256).digest()
		
		encoded_signature = self.base64url_encode(signature)
		token = f'{encoded_header}.{encoded_payload}.{encoded_signature}'

		return token

	def validateToken(self, token):
		"""
		takes a JWT token and returns True if the token is valid
		"""
		encoded_header, encoded_payload, encoded_signature = token.split('.')

		header = json.loads(base64.urlsafe_b64decode(encoded_header + '=' * (4 - len(encoded_header) % 4)))
		payload = json.loads(base64.urlsafe_b64decode(encoded_payload + '=' * (4 - len(encoded_payload) % 4)))
		signature = base64.urlsafe_b64decode(encoded_signature + '=' * (4 - len(encoded_signature) % 4))

		expected_signature = hmac.new(self.secret.encode('utf-8'), f'{encoded_header}.{encoded_payload}'.encode('utf-8'), hashlib.sha256).digest()
		if not hmac.compare_digest(signature, expected_signature):
			print ("Signature mismatch")
			return False, "Signature mismatch"

		if 'exp' in payload:
			expiration_time = datetime.utcfromtimestamp(payload['exp'])
			if expiration_time < datetime.now():
				print ("Token expired")
				return False, "Token expired"
		else:
			print ("Expiration time not found in payload")
			return False, "Expiration time not found in payload"
		print ("Token is valid")
		return True, "Token is valid"

	def getUserId(self, token):
		"""
		takes a JWT token and returns the user_id
		"""
		encoded_header, encoded_payload, encoded_signature = token.split('.')
		payload = json.loads(base64.urlsafe_b64decode(encoded_payload + '=' * (4 - len(encoded_payload) % 4)))
		user_id = payload['sub']
		return user_id
