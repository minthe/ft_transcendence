from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path

from backend_app.consumer import websocket

websocket_paths = ProtocolTypeRouter(
    {
        "websocket": URLRouter(
            [
                re_path(r'ws/init/(?P<user_id>\w+)/$', websocket.WebsocketConsumer.as_asgi()),
            ]
        ),
    }
)