from django.urls import path
from . import api_status as api_status
from . import api_account as api_account
from . import api_token as api_token
from . import api_avatar as api_avatar
from . import api_profile as api_profile
from . import api_second_factor as api_second_factor 

urlpatterns = [
    # Status
    path("status", api_status.heartbeat, name="status_heartbeat"),
	# Profile
	path('profile', api_profile.profile, name="profile"),
	# Avatar
	path('avatar', api_avatar.avatar, name="avatar"),
	# Account
	path("register", api_account.register, name="register"),
    path("login", api_account.login, name="login"),
	path("logout", api_account.logout, name="logout"),
	path('oauth2/login', api_account.oauth2_login, name="oauth2_login"),
  	path('oauth2/redirect', api_account.oauth2_redirect, name="oauth2_redirect"),
	# 2FA
	path('2fa', api_second_factor.second_factor, name="second_factor"),
	path('2fa/verify', api_second_factor.second_factor_verify, name="second_factor_verify"),
	# Token
	path("token", api_token.token, name="token"),
	path("token/existence", api_token.token_existence, name="token_existence"),
]
