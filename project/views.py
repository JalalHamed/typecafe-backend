from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project


class ProjectView(APIView):
    def get(self, request, *args, **kwargs):
        query = Project.objects.all()
        return Response(query)