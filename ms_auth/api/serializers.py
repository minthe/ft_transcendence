import base64, re
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

def validate_username(username):
	if len(username) < 2:
		raise ValidationError("Username must be at least 2 character long")
	if not username.isalnum():
		raise ValidationError("Username must be alphanumeric")
	return username

def validate_alias(alias):
	if len(alias) < 1:
		raise ValidationError("alias cannot be empty")
	return None

def validate_password(password):
	try:
		error_message = 'Password too weak'
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
	user_id_as_int = int(user_id)
	if not isinstance(user_id_as_int, int):
		raise ValidationError("user_id must be an integer")
	if isinstance(user_id, str):
		if not user_id.isdigit():
			raise ValidationError("user_id must be an integer")
	return None

def validate_2fa_code(code):
	code_as_int = int(code)
	if not isinstance(code_as_int, int):
		raise ValidationError("code must be digits only")
	if isinstance(code, str):
		if not code.isdigit():
			raise ValidationError("code must be digits only")
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