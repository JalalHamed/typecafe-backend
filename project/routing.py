from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path('ws/project-socket/', ProjectConsumer.as_asgi()),
]