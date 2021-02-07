from django.contrib import admin
from .models import *


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('description', 'client', 'created_at')


admin.site.register(Project, ProjectAdmin)