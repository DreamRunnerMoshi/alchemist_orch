# routing.py

from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from .consumer import ChatGPTConsumer
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

websocket_urlpatterns = [
    path('ws/chatgpt/', ChatGPTConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AllowedHostsOriginValidator(
        URLRouter(
            websocket_urlpatterns
        )
    )
})
