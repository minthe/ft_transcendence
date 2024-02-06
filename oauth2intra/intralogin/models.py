from django.db import models
from .managers import IntraUserOAuth2Manager

class IntraUser(models.Model):
	objects = IntraUserOAuth2Manager()

	id = models.BigIntegerField(primary_key=True)
	login = models.CharField(max_length=42, null=True)
	email = models.EmailField(null=True)
	first_name = models.CharField(max_length=42, null=True)
	last_name = models.CharField(max_length=42, null=True)
	last_login = models.DateTimeField(null=True)

	def is_authenticated(self, request):
		return True
