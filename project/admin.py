from django.contrib import admin
from .models import *


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('client', 'id', 'description', 'created_at', 'status')
    ordering = ['-created_at']
    search_fields = ['client', 'id', 'description']


admin.site.register(Project, ProjectAdmin)
admin.site.register(Offer)
