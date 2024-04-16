from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from user import views as user_views
from .exceptions import RateLimitExceeded, InvalidVerificationCode, ExpiredVerificationCode
from ft_jwt.ft_jwt.ft_jwt import FT_JWT

jwt = FT_JWT(settings.JWT_SECRET)

def generate_second_factor_dict():
    code = get_random_string(length=6, allowed_chars='0123456789')
    timestamp = timezone.now().isoformat()
    second_factor_dict = {'code': make_password(code), 'timestamp': timestamp, 'last_retry': timestamp}
    return second_factor_dict

def verify_verification_code(user_id, submitted_code):
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
                self.second_factor_retry_count = 0
                return True
            else:
                raise ExpiredVerificationCode('Code expired')
        code_data['last_retry'] = current_time.isoformat()
        self.second_factor_retry_count += 1
        return False
    except Exception as e:
        print(e)
        return False