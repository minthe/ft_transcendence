from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login_intra, name="login_intra"),
]
