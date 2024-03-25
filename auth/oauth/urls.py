from django.urls import path

from . import views

urlpatterns = [
    path("login", views.oauth_login, name="oauth_login"),
    path("redirect", views.oauth_authenticate, name="oauth_authenticate"),
]
