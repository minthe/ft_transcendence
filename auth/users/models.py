from django.db import models

class User(models.Model):
	sub = models.BigIntegerField(primary_key=True)
	intra_id = models.CharField(max_length=12, null=True)
	username = models.CharField(max_length=255, null=True)	
	password = models.CharField(max_length=255, null=True)
	email = models.CharField(max_length=255, null=True)
	image = models.CharField(max_length=255, null=True)
	jwt = models.CharField(max_length=255, null=True)

	sub = models.AutoField(primary_key=True)