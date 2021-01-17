from django.urls import path
from .views import RegistrationView

app_name = 'account'

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
]