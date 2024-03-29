from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *
from .models import Account

Account.objects.all().update(is_online=0)

app_name = 'account'

urlpatterns = [
    path('check-email/', CheckEmailView.as_view(), name='check-email'),
    path('confirm-email/', ConfirmEmailView.as_view(), name='confirm-email'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user-data/', UserDataView.as_view(), name='user-data'),
    path('update-displayname/', UpdateDisplaynameView.as_view(),
         name='update-displayname'),
    path('update-image/', UpdateProfileImageView.as_view(), name='update-image'),
    path('delete-image/', DeleteProfileImageView.as_view(), name='delete-image'),
    path('user-profile/', UserProfileView.as_view(), name='user-profile'),
    path('support-ticket/', SupportTicketView.as_view(), name='support-ticket'),
    path('support-message/', SupportMessageView.as_view(), name='support-message'),
    path('search-displayname/', SearchDisplaynameView.as_view(),
         name='search-displayname'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
