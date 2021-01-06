from django.contrib import admin
from . import models

@admin.register(models.Project)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'author', 'published')
