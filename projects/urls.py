from django.urls import path
from .views import ProjectsList, ProjectDetails

app_name = 'projects'

urlpatterns = [
    path('', ProjectsList.as_view(), name='listcreate'),
    path('<int:pk>/', ProjectDetails.as_view(), name='detailcreate'),
]