class VerificationError(Exception):
    pass
class RateLimitExceeded(VerificationError):
    pass
class InvalidVerificationCode(VerificationError):
	pass
class ExpiredVerificationCode(VerificationError):
	pass