from rest_framework import status
from rest_framework.permissions import *
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import *
from .serializers import *


class ProjectView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Project.objects.all()
    serializer_class = ProjectsSerializer
    pagination_class = PageNumberPagination


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
            return Response('lol. nice try', status=status.HTTP_403_FORBIDDEN)


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

    def get(self, request):
        offers = []
        for x in Project.objects.filter(client=request.user):
            offers.extend(Offer.objects.filter(project=x))
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DownloadedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        downloads = []
        for x in Downloaded.objects.filter(user=request.user):
            downloads.append(x.project.id)
        return Response(downloads, status=status.HTTP_200_OK)

    def post(self, request):
        if not Downloaded.objects.filter(user=request.user).filter(project=request.data['project']):
            serializer = DownloadedSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
        return Response(status=status.HTTP_201_CREATED)
