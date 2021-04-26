from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from .models import *


class ProjectsSerializer(serializers.ModelSerializer):
    client = serializers.SerializerMethodField('get_client_displayname')
    client_image = serializers.SerializerMethodField('get_client_image')
    client_email = serializers.SerializerMethodField('get_client_email')

    class Meta:
        model = Project
        fields = ['id', 'file', 'languages_and_additions', 'number_of_pages', 'delivery_deadline',
                  'type', 'description', 'created_at', 'client', 'client_email', 'client_image', 'status']

    def get_client_displayname(self, project):
        return project.client.displayname

    def get_client_image(self, project):
        if project.client.image:
            return '/media/' + str(project.client.image)

    def get_client_email(self, project):
        return project.client.email


class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'file', 'languages_and_additions', 'number_of_pages',
                  'delivery_deadline', 'type', 'description']


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['project', 'typist', 'offered_price']


class CreateOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['offered_price', 'project']
