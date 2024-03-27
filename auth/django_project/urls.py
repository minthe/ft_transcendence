from django.urls import include, path
from oauth2.views import oauth2_getToken, oauth2_getCode
from authManager.views import authManager_loginIntra

urlpatterns = [
	path('user/', include('users.urls')),
	path("oauth2/login", oauth2_getCode, name="oauth2_getCode"),
	path("oauth2/redirect", authManager_loginIntra, name="authManager_loginIntra"),
]
