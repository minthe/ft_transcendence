from django.urls import include, path

urlpatterns = [
    path('static/', include('api.urls')),
]
