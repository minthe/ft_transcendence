from django.contrib.auth import models

class IntraUserOAuth2Manager(models.UserManager):
	def create_new_intra_user(self, user):
		print('Inside Intra User Manager')
		new_user = self.create(
		id=user['id'],
		login=user['login'],
		email=user['email'],
		first_name=user['first_name'],
		last_name=user['last_name']
		)
		return new_user