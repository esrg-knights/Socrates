from django.contrib import admin

# Register your models here.
from account.models import DetailsModel, PasswordChangeRequestModel


class DetailsModelAdmin(admin.ModelAdmin):
    list_display = ("id",
                    "related_user",
                    "get_first_name",
                    "get_last_name",
                    "nickname",
                    "receive_broadcasts",
                    "is_softbanned"
                    )
    list_filter = ("theme", "is_softbanned", "instituut", "receive_broadcasts")
    search_fields = ("related_user",)

    def get_first_name(self, obj):
        return obj.related_user.first_name

    def get_last_name(self, obj):
        return obj.related_user.last_name


admin.site.register(DetailsModel, DetailsModelAdmin)
admin.site.register(PasswordChangeRequestModel)
