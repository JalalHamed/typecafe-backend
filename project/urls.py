from django.urls import path
from .views import *

app_name = 'project'

urlpatterns = [
    path('get-projects/', GetProjectsView.as_view(), name='get-projects'),
    path('all-projects/', AllProjectView.as_view(), name='all-projects'),
    path('open-projects/', OpenProjectsView.as_view(), name='open-projects'),
    path('in-progress-projects/', InProgressProjectsView.as_view(),
         name='in-progress-projects'),
    path('delivered-projects/', DeliveredProjectsView.as_view(),
         name='delivered-projects'),
    path('my-projects/', MyProjectsView.as_view(), name='my-projects'),
    path('create-project/', CreateProjectView.as_view(), name='createproject'),
    path('delete-project/', DeleteProjectView.as_view(), name='deleteproject'),
    path('create-offer/', CreateOfferView.as_view(), name='createoffer'),
    path('delete-offer/', DeleteOfferView.as_view(), name='delete-offer'),
    path('client-accept/', ClientAcceptView.as_view(), name='client-accept'),
    path('typist-declare-ready/', TypistDeclareReadyView.as_view(),
         name='typist-declare-ready'),
    path('reject-offer/', RejectOfferView.as_view(), name='reject-offer'),
    path('offers/', OffersView.as_view(), name='offers'),
    path('my-offers/', MyOffersView.as_view(), name='my-offers'),
    path('downloaded/', DownloadedView.as_view(), name='downloaded'),
    path('deliver/', DeliverTypedFile.as_view(), name='deliver-typed-file'),
]
