from django.contrib.auth.backends import BaseBackend
from django.core.exceptions import ObjectDoesNotExist
from .models import IntraUser

class IntraAuthenticationBackend(BaseBackend):
	def authenticate(self, request, user) -> IntraUser:
		try:
			return IntraUser.objects.get(id=user['id'])
		except ObjectDoesNotExist:
			print('User was not found. Saving...')
			new_user = IntraUser.objects.create_new_intra_user(user)
			print(new_user)
			return new_user

	def get_user(self, user_id):
		try:
			return IntraUser.objects.get(pk=user_id)
		except IntraUser.DoesNotExist:
			return None
