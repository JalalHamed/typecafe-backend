from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project
from .serializers import CreateProjectSerializer


class ProjectView(APIView):
    def get(self, request):
        return Response(Project.objects.all())
    

class CreateProject(APIView):
    def post(self, request):
        serializer = CreateProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)