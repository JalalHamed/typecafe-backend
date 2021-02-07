from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import Account
from .models import Project
from .serializers import *


class ProjectView(APIView):
    def get(self, request):
        serializer = ProjectsSerializer(Project.objects.all().order_by('-created_at'), many=True)
        dataList = serializer.data
        for index in range(len(dataList)):
            for key in dataList[index]:
                if key == 'client':
                    dataList[index][key] = Account.objects.get(id=dataList[index][key]).displayname
        return Response(dataList)


class CreateProjectView(APIView):
    def post(self, request):
        serializer = CreateProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(client=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)