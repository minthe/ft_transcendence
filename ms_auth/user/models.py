from django.db import models
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.utils.crypto import get_random_string
from exceptions import RateLimitExceeded, InvalidVerificationCode, ExpiredVerificationCode

class User(models.Model):
	user_id = models.BigIntegerField(primary_key=True)
	two_factor_enabled = models.BooleanField(null=True)
	two_factor_retry_count = models.IntegerField(null=True)
	two_factor_code = models.JSONField(db_column='two_factor_code', default=dict)
	intra_id = models.CharField(max_length=12, unique=True, null=True)
	username = models.CharField(max_length=255, unique=True, null=True)
	password = models.CharField(max_length=255, null=True)
	avatar = models.CharField(max_length=2000, null=True)
	email = models.CharField(max_length=255, unique=True, null=True)

	user_id = models.AutoField(primary_key=True)

	def set_password(self, plain_password):
		if plain_password:
			self.password = make_password(plain_password)
		else:
			self.password = self.generate_random_password()

	def check_password(self, plain_password):
		return check_password(plain_password, self.password)

	def generate_random_password(self, length=12):
		return get_random_string(length)

	def set_default_avatar(self):
		self.avatar = '${window.location.origin}/static/avatar/moon-dog.jpg'
  
	def generate_verification_code(self):
		try:
			code = get_random_string(length=6, allowed_chars='0123456789')
			timestamp = timezone.now().isoformat()
			self.twoFactorCode = {'code': make_password(code), 'timestamp': timestamp, 'last_retry': timestamp}
			self.save()
			return code
		except Exception as e:
			print(e)
			return None

	def verify_verification_code(self, submitted_code):
		try:
			current_time = timezone.now()
			code_data = self.twoFactorCode
			if code_data:
				code = code_data.get('code')
				# check rate limit
				last_retry_str = code_data.get('last_retry')
				last_retry = timezone.datetime.fromisoformat(last_retry_str)
				if last_retry + timezone.timedelta(seconds=5) > current_time:
					raise RateLimitExceeded('Rate limit exceeded')
				# check expiration time and code
				timestamp_str = code_data.get('timestamp')
				timestamp = timezone.datetime.fromisoformat(timestamp_str)
				expiration_time = timestamp + timezone.timedelta(seconds=300)
				if not check_password(submitted_code, code):
					raise InvalidVerificationCode('Invalid code')
				if current_time <= expiration_time and check_password(submitted_code, code):
					self.two_factor_retry_count = 0
					return True
				else:
					raise ExpiredVerificationCode('Code expired')
			code_data['last_retry'] = current_time.isoformat()
			self.two_factor_retry_count += 1
			return False
		except Exception as e:
			print(e)
			return False