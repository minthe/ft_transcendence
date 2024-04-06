from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
	sub = models.BigIntegerField(primary_key=True)
	intra_id = models.CharField(max_length=12, null=True)
	username = models.CharField(max_length=255, unique=True, null=True)
	password = models.CharField(max_length=255, null=True)
	email = models.CharField(max_length=255, unique=True, null=True)
	image = models.CharField(max_length=255, null=True)
	jwt = models.CharField(max_length=255, null=True)

	sub = models.AutoField(primary_key=True)

	def set_password(self, plain_password):
		self.password = make_password(plain_password)

	def check_password(self, plain_password):
		return check_password(plain_password, self.password)