from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import Account, SupportMessage, SupportTicket


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=8, style={'input_type': 'password'}, write_only=True, required=True)
    confirm_password = serializers.CharField(
        min_length=8, style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['displayname', 'email', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        account = Account(
            displayname=self.validated_data['displayname'],
            email=self.validated_data['email'],
        )
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError(
                {'password': ['passwords don\'t match.']})

        account.set_password(password)
        account.save()
        return account


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=256)
    password = serializers.CharField(min_length=8, write_only=True)
    access = serializers.CharField(max_length=256, read_only=True)
    refresh = serializers.CharField(max_length=256, read_only=True)

    class Meta:
        model = Account
        fields = ['email', 'password', 'access', 'refresh']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Password is not correct.')
        return {
            'email': user.email,
            'access': user.access,
            'refresh': user.refresh,
        }


class UpdateDisplaynameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['displayname']


class UpdateProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['image']


class SupportTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = ['client', 'status']


class SupportMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportMessage
        fields = ['client', 'ticket', 'message']


class SearchDisplaynameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'displayname', 'image', 'is_online', 'last_login']
