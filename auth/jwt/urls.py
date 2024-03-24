from django.urls import path

from . import views

urlpatterns = [
    path("", views.generate_jwt, name="generate_jwt"),
]
