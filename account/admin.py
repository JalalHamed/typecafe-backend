from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import *


class AccountAdmin(UserAdmin):
    list_display = ('displayname', 'email', 'credit', 'date_joined')
    ordering = ['-date_joined']
    search_fields = ['displayname', 'email']
    fieldsets = (
        ('Details', {'fields': ('displayname', 'email', 'picture',)}),
        ('Credits', {'fields': ('credit',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'displayname', 'credit', 'password1', 'password2', 'is_active')
        }),
    )


class ConfirmationCodeAdmin(admin.ModelAdmin):
    list_display = ('email', 'code', 'created_at')


admin.site.site_header = 'TypeCafe administartion'
admin.site.unregister(Group)
admin.site.register(Account, AccountAdmin)
admin.site.register(ConfirmationCode, ConfirmationCodeAdmin)
admin.site.register(SupportTicket)
admin.site.register(SupportMessage)