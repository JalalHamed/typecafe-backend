from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    path('check-email/', CheckEmailView.as_view(), name='check-email'),
    path('confirm-email/', ConfirmEmailView.as_view(), name='confirm-email'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile-image/', ProfileImageView.as_view(), name='profile-view')
]   