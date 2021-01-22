from random import randint
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegistrationSerializer
from .models import Account, ConfirmationCode


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
        email_address = request.data['email']
        user = Account.objects.filter(email__iexact=email_address)
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
                [email_address],
            )
            email.content_subtype = 'html'
            email.send(fail_silently=False)
            ConfirmationCode(code=confirm_code, email=email_address).save()
            return Response({'is_member': False})


class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        input_code = int(request.data['code'])
        email = request.data['email']
        confirm_request = ConfirmationCode.objects.filter(email__iexact=email).last()
        if input_code == confirm_request.code:
            return Response(True)
        else:
            return Response(False)