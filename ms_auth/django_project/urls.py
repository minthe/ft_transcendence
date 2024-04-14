from django.urls import include, path

urlpatterns = [
    path('user/', include('api.urls')),
]
