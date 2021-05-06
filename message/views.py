from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import *
from rest_framework.response import Response
from .models import *

class MessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response('ok', status=status.HTTP_200_OK)
        # message_query = Message.objects.filter(sender=request.user)
        # offers = []
        # for x in project_query:
        #     offer_query = Offer.objects.filter(project=x)
        #     offers.extend(offer_query)
        # serializer = OfferSerializer(offers, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
