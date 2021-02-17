from rest_framework import serializers
from .models import Project


class ProjectsSerializer(serializers.ModelSerializer):
    client = serializers.SerializerMethodField('get_client_displayname')
    client_picture = serializers.SerializerMethodField('get_client_picture')

    class Meta:
        model = Project
        fields = ['description', 'files', 'created_at', 'client', 'client_picture', 'status']

    def get_client_displayname(self, project):
        return project.client.displayname

    def get_client_picture(seld, project):
        if project.client.picture:
            return '/media/' + str(project.client.picture)


class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['description', 'files']
