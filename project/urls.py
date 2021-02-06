from django.urls import path
from .views import ProjectView, CreateProject

app_name = 'project'

urlpatterns = [
    path('projects/', ProjectView.as_view(), name='projects'),
    path('createproject/', CreateProject.as_view(), name='createproject')
]   