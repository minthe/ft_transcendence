from django.db import models

class User(models.Model):
	id = models.BigIntegerField(primary_key=True)
	intra = models.CharField(max_length=12, null=True)
	password = models.CharField(max_length=255, null=True)
	jwt_token = models.CharField(max_length=1024, null=True)

	id = models.AutoField(primary_key=True)