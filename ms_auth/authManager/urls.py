from django.urls import path
from . import views

urlpatterns = [
	path("logout", views.authManager_logout, name="authManager_logout"),
]
