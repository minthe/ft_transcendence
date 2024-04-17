from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from user import views as user_views
from ft_jwt.ft_jwt.ft_jwt import FT_JWT

jwt = FT_JWT(settings.JWT_SECRET)

def generate_second_factor_dict():
	code = get_random_string(length=6, allowed_chars='0123456789')
	timestamp = timezone.now().isoformat()
	second_factor_dict = {'code': make_password(code),
						  'timestamp': timestamp,
						  'last_retry': timestamp,
						  'second_factor_retry_count': 0}
	return second_factor_dict

def verify_verification_code(user_id, submitted_code):
	current_time = timezone.now()
	second_factor_dict = user_views.getValue(user_id, 'second_factor_dict')
	code = second_factor_dict.get('code', '')
	last_retry = timezone.datetime.fromisoformat(second_factor_dict.get('last_retry', '2000-01-01T00:00:00'))
	timestamp = timezone.datetime.fromisoformat(second_factor_dict.get('timestamp', '2000-01-01T00:00:00'))
	second_factor_retry_count = second_factor_dict.get('second_factor_retry_count', 0)

	if last_retry + timezone.timedelta(seconds=5) > current_time:
		second_factor_dict['last_retry'] = current_time.isoformat()
		second_factor_dict['second_factor_retry_count'] = second_factor_retry_count + 1
		user_views.updateValue(user_id, 'second_factor_dict', second_factor_dict)
		return False, 'Rate limit exceeded'

	if second_factor_retry_count >= 3:
		user_views.updateValue(user_id, 'second_factor_dict', second_factor_dict)
		return False, 'Maximum retries of 3 reached'

	if not check_password(submitted_code, code):
		second_factor_dict['last_retry'] = current_time.isoformat()
		second_factor_dict['second_factor_retry_count'] = second_factor_retry_count + 1
		user_views.updateValue(user_id, 'second_factor_dict', second_factor_dict)
		return False, 'Invalid code'

	expiration_time = timestamp + timezone.timedelta(seconds=300)
	if current_time > expiration_time:
		second_factor_dict['last_retry'] = current_time.isoformat()
		second_factor_dict['second_factor_retry_count'] = second_factor_retry_count + 1
		user_views.updateValue(user_id, 'second_factor_dict', second_factor_dict)
		return False, 'Code expired'

	second_factor_dict['second_factor_retry_count'] = 0
	user_views.updateValue(user_id, 'second_factor_dict', second_factor_dict)
	return True, None