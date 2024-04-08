from django.urls import path
from . import views as oauth2_views
from authManager import views as authManager_views

urlpatterns = [
	path("login", oauth2_views.getCode, name="getCode"),
	path("redirect", authManager_views.loginIntra, name="loginIntra"),
]
