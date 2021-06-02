from django.urls import path
from .views import *

app_name = 'project'

urlpatterns = [
    path('projects/', ProjectView.as_view(), name='projects'),
    path('my-projects/', MyProjectsView.as_view(), name='my-projects'),
    path('create-project/', CreateProjectView.as_view(), name='createproject'),
    path('delete-project/', DeleteProjectView.as_view(), name='deleteproject'),
    path('create-offer/', CreateOfferView.as_view(), name='createoffer'),
    path('delete-offer/', DeleteOfferView.as_view(), name='delete-offer'),
    path('client-accept/', ClientAcceptView.as_view(), name='client-accept'),
    path('typist-failed-to-accept/', TypistFailedToAccept.as_view(),
         name='typist-failed-to-accept'),
    path('accept-offer/', AcceptOfferView.as_view(), name='accepted-offer'),
    path('reject-offer/', RejectOfferView.as_view(), name='reject-offer'),
    path('offers/', OffersView.as_view(), name='offers'),
    path('offereds/', OfferedsView.as_view(), name='offered'),
    path('downloaded/', DownloadedView.as_view(), name='downloaded'),
]
