from rest_framework import serializers
from .models import Account, Email


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['username', 'email', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}


    def save(self):
        account = Account(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
        )
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError({'password': ['passwords don\'t match.']})

        account.set_password(password)
        account.save()
        return account


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ['email']

    def __str__(self):
        return self.email