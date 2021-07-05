import threading
from django.utils import timezone
from django.db.models import Q
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
        if project.client != request.user:
            return Response('lol. nice try', status=status.HTTP_403_FORBIDDEN)
        project.delete()
        return Response(status=status.HTTP_200_OK)


class CreateOfferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.data['offered_price'] < 1560:
            return Response('Ambition? No?', status=status.HTTP_403_FORBIDDEN)
        if request.user.project_todo:
            return Response(request.user.project_todo, status=status.HTTP_403_FORBIDDEN)
        project = Project.objects.get(id=request.data['project'])
        # earning per page with commission
        total_price = (request.data['offered_price'] * project.number_of_pages) + (
            request.data['offered_price'] * project.number_of_pages * 0.1)
        if request.user.credit < total_price:
            return Response('Not enough credits player, you already know.', status=status.HTTP_403_FORBIDDEN)
        if Project.objects.get(id=request.data['project']).client == request.user:
            return Response('Hmm.. interesting.', status=status.HTTP_403_FORBIDDEN)
        query = Offer.objects.filter(typist=request.user).filter(
            project=request.data['project'])
        if query:
            return Response({'error': 'You have already made a request for this project.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = CreateOfferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(total_price=total_price, project=Project.objects.get(
            id=request.data['project']), typist=request.user)
        Account.objects.filter(id=request.user.id).update(
            project_todo=request.data['project'])
        data = {
            'project': serializer.data['project'],
            'offered_price': serializer.data['offered_price'],
            'total_price': total_price,
            'id': serializer.data['id'],
            'status': serializer.data['status'],
            'typist_id': serializer.data['typist_id'],
        }
        return Response(data, status=status.HTTP_201_CREATED)


class DeleteOfferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        offer = Offer.objects.get(id=request.data['id'])
        if offer.typist != request.user:
            return Response('"How dare you try to take what you didn\'t help me to get?" -Eminem', status=status.HTTP_403_FORBIDDEN)
        offer.delete()
        return Response(status=status.HTTP_200_OK)


class ClientAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        offer = Offer.objects.get(id=request.data['id'])
        if offer.project.client != request.user:
            return Response('This is not your offer to accept.', status=status.HTTP_403_FORBIDDEN)
        query = Offer.objects.filter(typist=offer.typist)
        for x in query:
            if x.typist_ready:
                return Response('Typist is already busy with another project.', status=status.HTTP_400_BAD_REQUEST)
            if x.client_accept:
                return Response('Typist already has another project to declare ready for.', status=status.HTTP_400_BAD_REQUEST)
        offer.client_accept = timezone.now()
        offer.save()

        def CheckForTypistDeclareReady():
            offer = Offer.objects.get(id=request.data['id'])
            if not offer.typist_ready:
                offer.client_accept = None
                offer.save()

        timer = threading.Timer(30.0, CheckForTypistDeclareReady)
        timer.start()
        return Response(offer.client_accept, status=status.HTTP_200_OK)


class TypistDeclareReadyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        offer = Offer.objects.get(id=request.data['id'])
        if offer.typist != request.user:
            return Response('How that\'s gonna help?', status=status.HTTP_403_FORBIDDEN)
        if request.user.credit < offer.total_price:
            return Response('Not enough credits.', status=status.HTTP_402_PAYMENT_REQUIRED)
        if offer.project.client.credit < offer.total_price:
            return Response('Client Doesn\'t have enough credits.', status=status.HTTP_402_PAYMENT_REQUIRED)
        if offer.client_accept:
            Offer.objects.filter(project=offer.project).filter(
                ~Q(id=request.data['id'])).delete()  # ~Q means not equal
            Offer.objects.filter(typist=request.user).filter(
                ~Q(id=request.data['id'])).delete()
            offer.project.status = 'IP'
            offer.project.save()
            offer.status = 'ACC'
            offer.typist_ready = timezone.now()
            request.user.credit -= offer.total_price
            request.user.save()
            offer.project.client.credit -= offer.total_price
            offer.project.client.save()
            offer.save()
            return Response(offer.typist_ready, status=status.HTTP_200_OK)
        else:
            return Response('Too late unfortunately.', status=status.HTTP_400_BAD_REQUEST)


class RejectOfferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        offer = Offer.objects.get(id=request.data['id'])
        project_owner = offer.project.client
        if request.user != project_owner:
            return Response('How that helps?', status=status.HTTP_403_FORBIDDEN)
        offer.status = 'REJ'
        offer.save()
        return Response(status=status.HTTP_200_OK)


class OffersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        offers = []
        for x in Project.objects.filter(client=request.user):
            offers.extend(Offer.objects.filter(project=x))
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OfferedsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        offereds = []
        for x in Offer.objects.filter(typist=request.user):
            offereds.append({
                'id': x.id,
                'project': x.project.id,
                'offered_price': x.offered_price,
                'total_price': x.total_price,
                'created_at': x.created_at,
                'status': x.status,
                'typist_id': x.typist.id,
                'client_accept': x.client_accept,
                'typist_ready': x.typist_ready,
            })
        return Response(offereds, status=status.HTTP_200_OK)


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


class DeliverTypedFile(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        project = Project.objects.get(id=request.data['project'])
        typist = Offer.objects.get(project=project).typist
        if typist != request.user:
            return Response('You can\'t do this.', status=status.HTTP_401_UNAUTHORIZED)
        serializer = DeliverSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(project=project)
        return Response(status=status.HTTP_200_OK)
