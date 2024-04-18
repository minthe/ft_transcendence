"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

temp_app=get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from django.urls import re_path


# ik curly red looks bad but this is correct!!:
from backend_app.routing import websocket_paths

application = ProtocolTypeRouter({
    "http": temp_app,
    "websocket": AuthMiddlewareStack(
        websocket_paths
    ),
})
