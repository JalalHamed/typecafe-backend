from random import randint
from datetime import timedelta
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.utils.timezone import now
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from .models import *


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        res = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'email': user.email,
            'displayname': user.displayname,
        }
        return Response(res, status=status.HTTP_201_CREATED)


class CheckEmailView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Delete confirmation codes that are older than 1 day
        time_threshold = now() - timedelta(days=1)
        ConfirmationCode.objects.filter(created_at__lt=time_threshold).delete()
        # ---
        email_address = request.data['email']
        user = Account.objects.filter(email__iexact=email_address)
        if user.exists():
            return Response({'is_member': True})
        else:
            query = ConfirmationCode.objects.filter(email__iexact=email_address)
            if query.exists() and query.last().created_at + timedelta(minutes=3) > now():
                timeleft = query.last().created_at + timedelta(minutes=3) - now()
                return Response({'is_member': False, 'timeleft': timeleft})
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
                return Response({'is_member': False, 'timeleft': timedelta(minutes=3)})
                


class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        input_code = int(request.data['code'])
        email = request.data['email']
        confirm_request = ConfirmationCode.objects.filter(email__iexact=email).last()
        if input_code == confirm_request.code:
            return Response({'potato': 'potato'})
        else:
            return Response({'potato': 'potahto'})


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileImageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProfileImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK)


class SupportTicketView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SupportTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_201_CREATED)


class SupportMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SupportMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_201_CREATED)