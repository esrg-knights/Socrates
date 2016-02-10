from django.contrib import admin

# Register your models here.
from account.models import DetailsModel, PasswordChangeRequestModel


class DetailsModelAdmin(admin.ModelAdmin):
    list_display = ("id", "related_user")


admin.site.register(DetailsModel, DetailsModelAdmin)
admin.site.register(PasswordChangeRequestModel)