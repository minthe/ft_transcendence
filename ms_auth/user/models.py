from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
	userId = models.BigIntegerField(primary_key=True)
	two_factor_enabled = models.BooleanField(null=True)
	intra_id = models.CharField(max_length=12, unique=True, null=True)
	username = models.CharField(max_length=255, unique=True, null=True)
	password = models.CharField(max_length=255, null=True)
	avatar = models.CharField(max_length=2000, null=True)
	email = models.CharField(max_length=255, unique=True, null=True)

	userId = models.AutoField(primary_key=True)

	def set_password(self, plain_password):
		if plain_password:
			self.password = make_password(plain_password)
		else:
			self.password = self.generate_random_password()

	def check_password(self, plain_password):
		return check_password(plain_password, self.password)

	def generate_random_password(self, length=12):
		return get_random_string(length)