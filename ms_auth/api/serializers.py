import base64, re
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
	return None

def validate_password(password):
	try:
		error_message = 'Password too weak'
		print(password)
		if password.isalnum():
			raise ValidationError(error_message)
		pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&,;:])[A-Za-z\d@$!%*?&,;:]{8,}$'
		validator = RegexValidator(regex=pattern, message=error_message)
		validator(password)
	except ValidationError as e:
		raise ValidationError('Invalid password format: ' + str(e))
	return None

def validate_avatar(avatar):
	decoded_data = base64.b64decode(avatar)
	if len(decoded_data) > 2 * 1024 * 1024:
		raise ValidationError('File size over 2 MB limit')
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

def sanitize_input(input):
	substitute_char = '\u200B'
	sanitized = input.replace('\0', substitute_char).replace('\x00', substitute_char).replace('\u0000', substitute_char)
	sanitized = re.sub(r'\s+', substitute_char, sanitized)
	return sanitized

def desanitize_input(input):
	substitute_char = '\u200B'
	desanitized = input.replace(substitute_char, ' ')
	return desanitized