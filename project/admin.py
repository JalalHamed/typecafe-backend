from django.contrib import admin
from .models import *


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('client', 'id', 'description', 'created_at', 'status')
    ordering = ['-created_at']
    search_fields = ['client', 'id', 'description']


class OfferAdmin(admin.ModelAdmin):
    list_display = ('typist', 'project', 'offered_price',
                    'total_price', 'created_at', 'id', 'status')
    ordering = ['-created_at']
    search_fields = ['typist']


class DownloadedAdmin(admin.ModelAdmin):
    list_display = ('user', 'project')
    search_fields = ['user']


class DeliverAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'number_of_pages', 'delivered_at')
    search_fields = ['project']


admin.site.register(Project, ProjectAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Downloaded, DownloadedAdmin)
admin.site.register(Deliver, DeliverAdmin)
