from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from .models import *


class ProjectsSerializer(serializers.ModelSerializer):
    client = serializers.SerializerMethodField('get_client_displayname')
    client_picture = serializers.SerializerMethodField('get_client_picture')
    client_email = serializers.SerializerMethodField('get_client_email')

    class Meta:
        model = Project
        fields = ['id', 'file', 'languages_and_additions', 'number_of_pages', 'delivery_deadline', 'description', 'created_at', 'client', 'client_email', 'client_picture', 'status']

    def get_client_displayname(self, project):
        return project.client.displayname

    def get_client_picture(self, project):
        if project.client.picture:
            return '/media/' + str(project.client.picture)

    def get_client_email(self, project):
        return project.client.email


class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['file', 'languages_and_additions', 'number_of_pages', 'delivery_deadline', 'description']


class CreateOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['offered_price']
        