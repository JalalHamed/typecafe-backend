from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

app_name = 'account'

urlpatterns = [
    path('check-email/', CheckEmailView.as_view(), name='check-email'),
    path('confirm-email/', ConfirmEmailView.as_view(), name='confirm-email'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('update-displayname/', UpdateDisplaynameView.as_view(), name='update-displayname'),
    path('update-image/', UpdateProfileImageView.as_view(), name='profile-view'),
    path('user-data/', UserDataView.as_view(), name='user-data'),
    path('support-ticket/', SupportTicketView.as_view(), name='support-ticket'),
    path('support-message/', SupportMessageView.as_view(), name='support-message'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]   