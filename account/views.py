from random import randint
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template
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
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CheckEmailView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = CheckEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = Account.objects.filter(email=serializer.data['email'])
        if user.exists():
            return Response({'is_member': True})
        else:
            confirm_code = randint(10000000, 99999999)
            context_data = {'code': confirm_code}
            email_template = get_template('email.html').render(context_data)
            email = EmailMessage(
                'تایید آدرس ایمیل',
                email_template,
                settings.EMAIL_HOST_USER,
                [serializer.data['email']],
            )
            email.content_subtype = 'html'
            email.send(fail_silently=False)
            return Response({'is_member': False})