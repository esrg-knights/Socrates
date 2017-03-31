from django.contrib import admin
from .models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'category')
    list_filter = ('group', 'is_public', 'category')

# Register your models here.
admin.site.register(Event, EventAdmin)