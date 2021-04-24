from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path('ws/tc/', TcConsumer.as_asgi()),
]
