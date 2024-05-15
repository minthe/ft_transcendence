import base64
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

def validate_username(username):
	# TODO valentin add check if username already exists from 42 Intra
	if len(username) < 2:
		raise ValidationError("Username must be at least 2 character long")
	if not username.isalnum():
		raise ValidationError("Username must be alphanumeric")
	return username

def validate_alias(alias):
	# TODO valentin add check if alias already exists from 42 Intra
	if len(alias) < 1:
		raise ValidationError("alias cannot be empty")
	if not alias.isalnum():
		raise ValidationError("alias must be alphanumeric")
	return None


def validate_password(password):
	try:
		print(password)
		pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&,;:])[A-Za-z\d@$!%*?&,;:]{8,}$'
		validator = RegexValidator(regex=pattern, message='Password must contain at least 1 uppercase letter, 1 lowercase letter, 1 digit, 1 of these special characters in []: [A-Za-z\d@$!%*?&,;:], and be at least 8 characters long')
		validator(password)
	except ValidationError as e:
		raise ValidationError('Invalid password format: ' + str(e))
	return None

def validate_avatar(avatar):
	decoded_data = base64.b64decode(avatar)
	if len(decoded_data) > 5 * 1024 * 1024:
		raise ValidationError('File size over 5 MB limit')
	return None

def validate_user_id(user_id):
	if not user_id.isnumeric():
		raise ValidationError("user_id must be numeric")
	return None

def validate_2fa_code(code):
	if not code.isnumeric():
		raise ValidationError("code must be numeric")
	if not len(code) == 6:
		raise ValidationError('code must be 6 digits long')
	return None