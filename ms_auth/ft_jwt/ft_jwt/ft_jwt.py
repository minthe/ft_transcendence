import hashlib, base64, hmac, json
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.utils import timezone
from functools import wraps

class FT_JWT:

	def __init__(self, secret):
		self.secret = secret

	def base64url_encode(self, input):
		return base64.urlsafe_b64encode(input).decode('utf-8').rstrip('=')

	def createToken(self, sub):
		"""
		takes a json object and returns a JWT token
		- token contains user_id and expiration date (1 day)
		"""
		try:
			current_time = timezone.now().replace(tzinfo=None)
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
		except Exception as e:
			error_message = str(e)
			print(f"An error occurred: {error_message}")
			return JsonResponse({'message': error_message}, status=500)

	def validateToken(self, token):
		"""
		takes a JWT token and returns True if the token is valid
		"""
		try:
			encoded_header, encoded_payload, encoded_signature = token.split('.')
			header = json.loads(base64.urlsafe_b64decode(encoded_header + '=' * (4 - len(encoded_header) % 4)))
			payload = json.loads(base64.urlsafe_b64decode(encoded_payload + '=' * (4 - len(encoded_payload) % 4)))
			signature = base64.urlsafe_b64decode(encoded_signature + '=' * (4 - len(encoded_signature) % 4))

			expected_signature = hmac.new(self.secret.encode('utf-8'), f'{encoded_header}.{encoded_payload}'.encode('utf-8'), hashlib.sha256).digest()
			if not hmac.compare_digest(signature, expected_signature):
				print ("Signature mismatch")
				return False, "Signature mismatch"

			if 'exp' in payload:
				expiration_time = datetime.fromtimestamp(payload['exp'])
				if expiration_time < datetime.now().replace(tzinfo=None):
					print ("Token expired")
					return False, "Token expired"
			else:
				print ("Expiration time not found in payload")
				return False, "Expiration time not found in payload"
			return True, "Token is valid"
		except Exception as e:
			error_message = str(e)
			print(f"An error occurred: {error_message}")
			return JsonResponse({'message': error_message}, status=500)

	def getUserId(self, token):
		"""
		takes a JWT token and returns the user_id
		"""
		try:
			encoded_header, encoded_payload, encoded_signature = token.split('.')
			payload = json.loads(base64.urlsafe_b64decode(encoded_payload + '=' * (4 - len(encoded_payload) % 4)))
			user_id = payload['sub']
			return user_id
		except Exception as e:
			error_message = str(e)
			print(f"An error occurred: {error_message}")
			return JsonResponse({'message': error_message}, status=500)

	def token_required(self, f):
		@wraps(f)
		def decorated(request, *args, **kwargs):
			try:
				token = request.COOKIES.get('jwt_token')

				if not token:
					return JsonResponse({'message': "Unauthorized (token missing)"}, status=401)

				jwt_instance = FT_JWT(self.secret)
				is_valid, message = jwt_instance.validateToken(token)
				if not is_valid:
					return JsonResponse({'message': "Unauthorized (token invalid)"}, status=401)
				user_id = jwt_instance.getUserId(token)
				request.user_id = user_id
				return f(request, *args, **kwargs)
			except Exception as e:
				error_message = str(e)
				print(f"An error occurred: {error_message}")
				return JsonResponse({'message': error_message}, status=500)
		return decorated