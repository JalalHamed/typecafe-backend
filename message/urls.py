from django.urls import path
from .views import *

app_name = 'message'

urlpatterns = [
    path('', MessagesView.as_view(), name='messages'),
    path('read-messages/', ReadMessages.as_view(), name='send'),
]
