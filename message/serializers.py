from rest_framework import serializers
from .models import *


class SenderSerializer(serializers.ModelSerializer):
    sor = serializers.SerializerMethodField('get_sent_or_received')
    user = serializers.SerializerMethodField('get_user_displayname')
    user_id = serializers.SerializerMethodField('get_user_id')
    user_image = serializers.SerializerMethodField('get_user_image')
    user_is_online = serializers.SerializerMethodField('get_user_is_online')
    user_last_login = serializers.SerializerMethodField('get_user_last_login')

    class Meta:
        model = Message
        fields = ['id', 'sor', 'user', 'user_id', 'user_image', 'user_is_online', 'user_last_login', 'content', 'issue_date', 'is_read']

    def get_sent_or_received(self, message):
        return 'received'

    def get_user_displayname(self, message):
        return message.sender.displayname
    
    def get_user_id(self, message):
        return message.sender.id

    def get_user_image(self, message):
        if message.sender.image:
            return '/media/' + str(message.sender.image)
    
    def get_user_is_online(self, message):
        return message.sender.is_online
    
    def get_user_last_login(self, message):
        return message.sender.last_login


class ReceiverSerializer(serializers.ModelSerializer):
    sor = serializers.SerializerMethodField('get_sent_or_received')
    user = serializers.SerializerMethodField('get_user_displayname')
    user_id = serializers.SerializerMethodField('get_user_id')
    user_image = serializers.SerializerMethodField('get_user_image')
    user_is_online = serializers.SerializerMethodField('get_user_is_online')
    user_last_login = serializers.SerializerMethodField('get_user_last_login')

    class Meta:
        model = Message
        fields = ['id', 'sor', 'user', 'user_id', 'user_image', 'user_is_online', 'user_last_login', 'content', 'issue_date', 'is_read']

    def get_sent_or_received(self, message):
        return 'sent'

    def get_user_displayname(self, message):
        return message.receiver.displayname
    
    def get_user_id(self, message):
        return message.receiver.id
    
    def get_user_image(self, message):
        if message.receiver.image:
            return '/media/' + str(message.receiver.image)
    
    def get_user_is_online(self, message):
        return message.receiver.is_online
    
    def get_user_last_login(self, message):
        return message.receiver.last_login