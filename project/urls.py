from django.urls import path
from .views import *

app_name = 'project'

urlpatterns = [
    path('projects/', ProjectView.as_view(), name='projects'),
    path('mine/', MineView.as_view(), name='mine'),
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
