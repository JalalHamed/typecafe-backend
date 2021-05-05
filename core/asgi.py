import os
from django.urls import path
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from .token_auth import JwtAuthMiddlewareStack
from .consumers import TcConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JwtAuthMiddlewareStack(URLRouter([
        path('ws/tc/', TcConsumer.as_asgi()),
    ])),
})
