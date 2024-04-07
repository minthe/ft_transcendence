from django.urls import include, path

urlpatterns = [
	path('', include('authManager.urls')),
	path('users/', include('users.urls')),
	path('oauth2/', include('oauth2.urls')),
]
