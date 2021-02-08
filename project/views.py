from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project
from .serializers import *


class ProjectView(APIView):
    def get(self, request):
        serializer = ProjectsSerializer(Project.objects.all(), many=True)
        return Response(serializer.data)


class CreateProjectView(APIView):
    def post(self, request):
        serializer = CreateProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(client=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)