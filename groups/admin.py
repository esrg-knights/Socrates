from django.contrib import admin
from .models import GroupDetails

class GroupDetailAdmin(admin.ModelAdmin):
    list_display = ('related_user', 'name', 'shorthand')

# Register your models here.
admin.site.register(GroupDetails, GroupDetailAdmin)