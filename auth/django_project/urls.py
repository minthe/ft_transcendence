from django.urls import include, path
from intralogin import views

urlpatterns = [
	path('', include('intralogin.urls')),
]
