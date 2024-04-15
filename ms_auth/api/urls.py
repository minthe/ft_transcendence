from django.urls import include, path
from . import api_status as api_status
from . import api_user as api_user
from . import api_token as api_token
from . import api_oauth2 as api_oauth2
from user import views as user_views
from oauth2 import views as oauth2_views

urlpatterns = [
    # Status
    path("status", api_status.heartbeat, name="status_heartbeat"),
	path("token/existence", api_token.token_existence, name="token_existence"),

	# Account
	path("register", api_user.register, name="register"),
    path("login", api_user.login, name="login"),
	path("logout", api_user.logout, name="logout"),

	# Authentication
	path('oauth2/login', api_oauth2.oauth2_login, name="oauth2_login"),
  	path('oauth2/redirect', oauth2_views.oauth2_redirect, name="oauth2_redirect"),

	# 2fa
	# /user/verifyTwoFactorCode
	path('<int:user_id>/2fa/update', api_user.second_factor_update, name="second_factor"),
 	path('<int:user_id>/2fa/code', api_user.second_factor_code, name="second_factor"),

	# User
	path('me', user_views.getId, name="getId"), # TODO @valentin return all user data and change function name to me
	path('<int:user_id>/avatar', api_user.avatar, name="avatar"),
]
