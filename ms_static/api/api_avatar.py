import json, base64
from django.conf import settings
from django.core.files.base import ContentFile
from django.http import JsonResponse
from urllib.request import Request, urlopen
from ft_jwt.ft_jwt import FT_JWT

jwt = FT_JWT(settings.JWT_SECRET)

@jwt.token_required
def avatar(request):
	pass