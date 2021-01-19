from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegistrationSerializer, CheckEmailSerializer
from .models import Account


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_mail(
            'HEY man',
            'THIS IS FOOKIN STUPID MAN, YOU WHAM SAYIN???',
            'typecafeir@gmail.com',
            ['memlobarze@nedoz.com'],
            fail_silently=False
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CheckEmailView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = CheckEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = Account.objects.filter(email=serializer.data['email'])
        if user.exists():
            return Response({'is_member': True, 'username': user.first().username})
        else:
            return Response({'is_member': False})