from django.utils.crypto import get_random_string
from django.utils import timezone
from user import views as user_views
import datetime

def generate_second_factor_dict():
	code = get_random_string(length=6, allowed_chars='0123456789')
	timestamp = timezone.now().replace(tzinfo=None).isoformat()
	second_factor_dict = {'code': code,  # TODO valentin store in memory cache
						  'timestamp': timestamp,
						  'last_retry': timestamp}
	return second_factor_dict

def verify_verification_code(user_id, submitted_code):
	current_time = timezone.now().replace(tzinfo=None)
	second_factor_dict = user_views.getValue(user_id, 'second_factor_dict')
	code = second_factor_dict.get('code')
	last_retry = timezone.datetime.fromisoformat(second_factor_dict.get('last_retry')).replace(tzinfo=None)
	timestamp_str = second_factor_dict.get('timestamp', '')

	if timestamp_str:
		timestamp = datetime.datetime.fromisoformat(timestamp_str).replace(tzinfo=None)
	else:
		timestamp = datetime.datetime.min
	if last_retry + timezone.timedelta(seconds=3) > current_time:
		second_factor_dict['last_retry'] = current_time.isoformat()
		user_views.updateValue(user_id, 'second_factor_dict', second_factor_dict)
		return False, 'Rate limit exceeded'
	if not submitted_code == code:
		print(f"submitted_code: {submitted_code}, code: {code}")
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