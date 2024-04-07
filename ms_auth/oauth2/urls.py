from django.urls import path
from . import views
from authManager.views import authManager_loginIntra

urlpatterns = [
	path("login", views.oauth2_getCode, name="oauth2_getCode"),
	path("redirect", authManager_loginIntra, name="authManager_loginIntra"),
]
