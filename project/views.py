from django.utils import timezone
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
        try:
            query = Offer.objects.filter(
                typist=request.user).get(status="ACC")
            return Response(query.project.id, status=status.HTTP_403_FORBIDDEN)
        except:
            pass
        project = Project.objects.get(id=request.data['project'])
        # earning per page with commission
        eppwc = request.data['offered_price'] - \
            request.data['offered_price'] * 0.1
        total_price = eppwc * project.number_of_pages
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
        serializer.save(project=Project.objects.get(
            id=request.data['project']), typist=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
        offer.client_accept = timezone.now()
        offer.save()
        return Response(offer.client_accept, status=status.HTTP_200_OK)


class TypistFailedToAccept(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        offer = Offer.objects.get(id=request.data['id'])
        if offer.typist != request.user:
            return Response('Hm nice try.', status=status.HTTP_403_FORBIDDEN)
        offer.client_accept = None
        offer.save()
        return Response(status=status.HTTP_200_OK)


class AcceptOfferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        offer = Offer.objects.get(id=request.data['id'])
        project_owner = offer.project.client
        total_price = offer.offered_price * offer.project.number_of_pages
        typist_total_price = total_price - total_price * 0.1
        client_total_price = total_price + total_price * 0.1
        if request.user != project_owner:
            return Response('You know you can\'t do that right?', status=status.HTTP_403_FORBIDDEN)
        if request.user.credit < client_total_price:
            return Response('Not enough credits.', status=status.HTTP_402_PAYMENT_REQUIRED)
        if offer.typist.credit < typist_total_price:
            return Response('Typist Doesn\'t have enough credits.', status=status.HTTP_402_PAYMENT_REQUIRED)
        request.user.credit -= client_total_price
        request.user.save()
        offer.typist.credit -= typist_total_price
        offer.typist.save()
        offer.status = 'ACC'
        offer.save()
        offer.project.status = 'IP'
        offer.project.save()
        projectOffers = Offer.objects.filter(project=offer.project)
        for x in projectOffers:
            if x.id != request.data['id']:
                x.delete()
        typistOffers = Offer.objects.filter(typist=offer.typist)
        for x in typistOffers:
            if x.id != request.data['id']:
                x.delete()
        return Response({'credit': request.user.credit}, status=status.HTTP_200_OK)


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
                'created_at': x.created_at,
                'status': x.status,
                'typist_id': x.typist.id,
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
