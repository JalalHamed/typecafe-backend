from django.contrib import admin
from .models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'issue_date', 'is_read', 'id')

admin.site.register(Message, MessageAdmin)
