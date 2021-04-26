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
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyProjectsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProjectsSerializer(
            Project.objects.filter(client=request.user), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(client=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeleteProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        project = Project.objects.get(id=request.data['id'])
        if project.client == request.user:
            project.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response('lol. nice try', status=status.HTTP_401_UNAUTHORIZED)


class CreateOfferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        query = Offer.objects.filter(typist=request.user).filter(
            project=request.data['project'])
        if query:
            return Response({'error': 'You have already made a request for this project.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CreateOfferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(project=Project.objects.get(
            id=request.data['project']), typist=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OffersView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        project = Project.objects.get(id=request.data['project_id'])
        if request.user == project.client:
            serializer = OfferSerializer(
                Offer.objects.filter(project=project), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'You are not authorized to access this information.'}, status=status.HTTP_403_FORBIDDEN)
