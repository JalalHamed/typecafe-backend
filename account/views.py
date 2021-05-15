from random import randint
from datetime import timedelta
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.utils.timezone import now
from django.contrib.auth.models import update_last_login
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
            'access': str(refresh.access_token),
            'refresh': str(refresh),
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
            query = ConfirmationCode.objects.filter(
                email__iexact=email_address)
            if query.exists() and query.last().created_at + timedelta(minutes=3) > now():
                timeleft = query.last().created_at + timedelta(minutes=3) - now()
                return Response({'is_member': False, 'timeleft': timeleft})
            else:
                confirm_code = randint(10000000, 99999999)
                context_data = {'code': confirm_code}
                email_template = get_template(
                    'email.html').render(context_data)
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
        confirm_request = ConfirmationCode.objects.filter(
            email__iexact=email).last()
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


class UserProfileView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = Account.objects.get(id=request.data['id'])
        data = {
            'typist_successful_projects': user.typist_successful_projects,
            'typist_unsuccessful_projects': user.typist_unsuccessful_projects,
            'ontime_delivery': user.ontime_delivery,
            'client_successful_projects': user.client_successful_projects,
            'client_unsuccessful_projects': user.client_unsuccessful_projects,
            'ontime_payment': user.ontime_payment,
            'is_online': user.is_online,
            'last_login': user.last_login,
        }
        return Response(data, status=status.HTTP_200_OK)


class UserDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user.is_online = True
        user.save(update_fields=['is_online'])
        pic = ""
        if user.image:
            pic = '/media/' + str(user.image)
        data = {
            'displayname': user.displayname,
            'credit': user.credit,
            'email': user.email,
            'id': user.id,
            'image': pic,
            'typist_successful_projects': user.typist_successful_projects,
            'typist_unsuccessful_projects': user.typist_unsuccessful_projects,
            'ontime_delivery': user.ontime_delivery,
            'client_successful_projects': user.client_successful_projects,
            'client_unsuccessful_projects': user.client_unsuccessful_projects,
            'ontime_payment': user.ontime_payment,
        }
        return Response(data, status=status.HTTP_200_OK)


class UpdateDisplaynameView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = UpdateDisplaynameSerializer(
            request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProfileImageView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = UpdateProfileImageSerializer(
            request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteProfileImageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        request.user.image.delete()
        return Response('Profile picture deleted.', status=status.HTTP_200_OK)


class UserDisconnectView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user.is_online = False
        user.save(update_fields=['is_online'])
        update_last_login(None, user)      
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


class SearchDisplaynameView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        query = Account.objects.filter(displayname__istartswith=request.data['search'])
        serializer = SearchDisplaynameSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)