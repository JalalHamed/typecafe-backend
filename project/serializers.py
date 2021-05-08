from rest_framework import serializers
from .models import *


class ProjectsSerializer(serializers.ModelSerializer):
    client = serializers.SerializerMethodField('get_client_displayname')
    client_image = serializers.SerializerMethodField('get_client_image')
    client_id = serializers.SerializerMethodField('get_client_id')
    client_is_online = serializers.SerializerMethodField('get_client_is_online')
    client_last_login = serializers.SerializerMethodField('get_client_last_login')

    class Meta:
        model = Project
        fields = ['id', 'file', 'languages_and_additions', 'number_of_pages', 'delivery_deadline',
                  'type', 'description', 'created_at', 'client', 'client_id', 'client_image', 'client_is_online', 'client_last_login', 'status']

    def get_client_displayname(self, project):
        return project.client.displayname

    def get_client_image(self, project):
        if project.client.image:
            return '/media/' + str(project.client.image)

    def get_client_id(self, project):
        return project.client.id
    
    def get_client_is_online(self, project):
        return project.client.is_online

    def get_client_last_login(self, project):
        return project.client.last_login


class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'file', 'languages_and_additions', 'number_of_pages',
                  'delivery_deadline', 'type', 'description']


class OfferSerializer(serializers.ModelSerializer):
    typist = serializers.SerializerMethodField('get_typist_displayname')
    typist_image = serializers.SerializerMethodField('get_typist_image')
    typist_id = serializers.SerializerMethodField('get_typist_id')

    class Meta:
        model = Offer
        fields = ['id', 'project', 'typist', 'typist_image', 'typist_id', 'status', 'offered_price', 'created_at']
    
    def get_typist_displayname(self, offer):
        return offer.typist.displayname

    def get_typist_image(self, offer):
        if offer.typist.image:
            return '/media/' + str(offer.typist.image)

    def get_typist_id(self, offer):
        return offer.typist.id

class CreateOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['id', 'offered_price', 'project']


class DownloadedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Downloaded
        fields = ['project']
