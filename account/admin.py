from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Account, ConfirmationCode


class ConfirmationCodeAdmin(admin.ModelAdmin):
    list_display = ('email', 'code', 'created_at')

admin.site.site_header = 'TypeCafe administartion'
admin.site.unregister(Group)
admin.site.register(Account)
admin.site.register(ConfirmationCode, ConfirmationCodeAdmin)