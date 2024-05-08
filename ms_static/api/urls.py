from django.urls import path
from . import api_status as api_status
from . import api_avatar as api_avatar

urlpatterns = [
    # Status
    path("status", api_status.heartbeat, name="status_heartbeat"),
	# Avatar
	path('avatar', api_avatar.avatar, name="avatar"),
]
