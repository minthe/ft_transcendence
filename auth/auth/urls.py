from django.urls import path
from intralogin import views

urlpatterns = [
    path('auth/user', views.get_authenticated_user, name='get_authenticated_user'),
	path('auth/login', views.intra_login, name='auth_login'),
	path('auth/login/redirect', views.intra_login_redirect, name='auth_login_redirect')
]
