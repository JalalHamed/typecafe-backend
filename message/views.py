from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import *
from rest_framework.response import Response
from .models import *
from .serializers import *


class MessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        receiver = Message.objects.filter(receiver=request.user)
        sender = Message.objects.filter(sender=request.user)
        sender_serializer = SenderSerializer(receiver, many=True)
        receiver_serializer = ReceiverSerializer(sender, many=True)
        serializer = sender_serializer.data + receiver_serializer.data
        return Response(serializer, status=status.HTTP_200_OK)
        
    def post(self, request):
        if request.data['receiver'] == request.user.id:
            return Response('Yeah already prevented but nice try tho 👍', status=status.HTTP_400_BAD_REQUEST)
        serializer = CreateMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReadMessages(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        query = Message.objects.filter(receiver=request.user).filter(sender=request.data['sender_id'])
        for x in query:
            x.is_read = True
            x.save()
        return Response(status=status.HTTP_200_OK)