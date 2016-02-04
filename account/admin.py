from django.contrib import admin

# Register your models here.
from account.models import DetailsModel

class DetailsModelAdmin(admin.ModelAdmin):
    list_display = ("id", "related_user")


admin.site.register(DetailsModel, DetailsModelAdmin)
