from django.urls import path
from .views import *

app_name = 'project'

urlpatterns = [
    path('projects/', ProjectView.as_view(), name='projects'),
    path('createproject/', CreateProjectView.as_view(), name='createproject'),
    path('deleteproject/', DeleteProjectView.as_view(), name='deleteproject'),
    path('createoffer/', CreateOfferView.as_view(), name='createoffer'),
    path('myprojects/', MyProjectsView.as_view(), name='my-projects'),
    path('offers/', OffersView.as_view(), name='get-offers'),
]
