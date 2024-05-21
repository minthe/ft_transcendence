from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('game/admin', admin.site.urls),
    path('', include('backend_app.urls'))
]

