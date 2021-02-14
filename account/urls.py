from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views

app_name = 'account'

urlpatterns = [
    path('check-email/', CheckEmailView.as_view(), name='check-email'),
    path('confirm-email/', ConfirmEmailView.as_view(), name='confirm-email'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]   