from django.urls import include, path
from . import views as authManager_views
from user import views as user_views

urlpatterns = [
	path('oauth2/', include('oauth2.urls')),
    path("login", authManager_views.login, name="login"),
	path("logout", authManager_views.logout, name="logout"),
 
	# for frontend
	path("token/existence", authManager_views.checkTokenExist, name="token/existence"),
 
	# users
	path("me", user_views.getId, name="getId"),
]
