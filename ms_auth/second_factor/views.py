import datetime
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.utils import timezone
from user import views as user_views
from mail import views as mail_views

def store_2fa_code(user_id, code):
	cache.set(f'2fa_code_{user_id}', code, 300)

def get_2fa_code(user_id):
	return cache.get(f'2fa_code_{user_id}')

def generate_second_factor_dict(code):
	timestamp = timezone.now().replace(tzinfo=None).isoformat()
	hashed_code = make_password(code)
	second_factor_dict = {'code': hashed_code,
						  'timestamp': timestamp,
						  'last_retry': timestamp}
	return second_factor_dict

def create_2fa(user_id):
	code = get_random_string(length=6, allowed_chars='0123456789')
	store_2fa_code(user_id, code)
	second_factor_dict = generate_second_factor_dict(code)
	username = user_views.getValue(user_id, 'username')
	user_views.updateValue(user_id, 'second_factor_dict', second_factor_dict)
	mail_views.send_verification_email(username, code, user_views.getValue(user_id, 'email'))

def verify_2fa(user_id, submitted_code):
	current_time = timezone.now().replace(tzinfo=None)
	second_factor_dict = user_views.getValue(user_id, 'second_factor_dict')
	last_retry = timezone.datetime.fromisoformat(second_factor_dict.get('last_retry')).replace(tzinfo=None)
	timestamp_str = second_factor_dict.get('timestamp', '')
	stored_code = get_2fa_code(user_id)

	if timestamp_str:
		timestamp = datetime.datetime.fromisoformat(timestamp_str).replace(tzinfo=None)
	else:
		timestamp = datetime.datetime.min
	if last_retry + timezone.timedelta(seconds=3) > current_time:
		second_factor_dict['last_retry'] = current_time.isoformat()
		user_views.updateValue(user_id, 'second_factor_dict', second_factor_dict)
		return False, 'Rate limit exceeded'
	if not submitted_code == stored_code:
		print(f"submitted_code: {submitted_code}, code: {stored_code}")
		second_factor_dict['last_retry'] = current_time.isoformat()
		user_views.updateValue(user_id, 'second_factor_dict', second_factor_dict)
		return False, 'Invalid code'

	expiration_time = timestamp + timezone.timedelta(seconds=300)
	if current_time > expiration_time:
		second_factor_dict['last_retry'] = current_time.isoformat()
		user_views.updateValue(user_id, 'second_factor_dict', second_factor_dict)
		return False, 'Code expired'

	user_views.updateValue(user_id, 'second_factor_dict', second_factor_dict)
	return True, None