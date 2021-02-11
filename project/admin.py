from django.contrib import admin
from .models import *


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'description', 'created_at', 'status')
    ordering = ['-created_at']
    search_fields = ['client', 'description']

admin.site.register(Project, ProjectAdmin)