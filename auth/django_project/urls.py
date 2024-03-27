from django.urls import include, path
from intra42.views import intra42_login
from oauth2.views import oauth2_get_token, oauth2_request_code

urlpatterns = [
	path('user/', include('users.urls')),
	path("oauth2/login", oauth2_request_code, name="oauth2_request_code"),
	path("oauth2/redirect", intra42_login, name="intra42_login"),
]
