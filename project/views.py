from rest_framework import status
from rest_framework.permissions import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *


class ProjectView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        serializer = ProjectsSerializer(Project.objects.all(), many=True)
        return Response(serializer.data)


class CreateProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(client=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreateOfferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateOfferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(project=Project.objects.get(id=request.data['project_id']))
        return Response(serializer.data, status=status.HTTP_201_CREATED)
