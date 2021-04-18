from django.urls import path
from .consumers import ProjectConsumer

websocket_urlpatterns = [
    path('ws/project/', ProjectConsumer.as_asgi()),
]
