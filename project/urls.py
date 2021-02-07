from django.urls import path
from .views import ProjectView, CreateProjectView

app_name = 'project'

urlpatterns = [
    path('projects/', ProjectView.as_view(), name='projects'),
    path('createproject/', CreateProjectView.as_view(), name='createproject')
]   