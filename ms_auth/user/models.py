from django.conf import settings
from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
	id	= models.AutoField(primary_key=True)
	user_id = models.SmallIntegerField(unique=True, null=True)
	second_factor_enabled = models.BooleanField(default=False)
	second_factor_dict = models.JSONField(db_column='second_factor_dict', default=dict)
	intra_id = models.CharField(max_length=12, unique=True, null=True)
	username = models.CharField(max_length=255, unique=True, null=True)
	password = models.CharField(max_length=255, null=True)
	avatar = models.CharField(max_length=2000, null=True)
	email = models.CharField(max_length=255, unique=True, null=True)
	alias = models.CharField(max_length=255, unique=True, null=True)

	def set_password(self, plain_password):
		if plain_password:
			self.password = make_password(plain_password)
		else:
			self.password = self.generate_random_password()

	def check_password(self, plain_password):
		return check_password(plain_password, self.password)

	def generate_random_password(self, length=12):
		return get_random_string(length)

	def set_default_avatar(self):
		self.avatar = f"https://{settings.CURRENT_HOST}{settings.LOC_AVATAR}{settings.AVATAR_DEFAULT}"

	@classmethod
	def get_highest_user_id(cls):
		highest_id = cls.objects.aggregate(max_id=models.Max('user_id'))['max_id']
		return highest_id if highest_id is not None else 0