# Register your models here.
from django.contrib import admin

from .models import *


class DiningListAdmin(admin.ModelAdmin):
    list_display = ("id", "relevant_date", "owner")
    list_filter = ('relevant_date', "owner")
    fieldsets = (
        ("Relevante gegevens", {
            'fields': ('owner',)
        }),
        ("Datum", {
            'fields': ('relevant_date', 'closing_time')
        }),
    )

    actions = ["assign_dishes", "assign_dishes_weighted"]

    def assign_dishes(modeladmin, request, queryset):
        for item in queryset:
            print(item)
            item.assign_dishes(randomChoices=True)

    def assign_dishes_weighted(modeladmin, request, queryset):
        for item in queryset:
            print(item)
            item.assign_dishes(randomChoices=False)

    assign_dishes_weighted.short_description = "Assign dishes based on statistics"
    assign_dishes.short_description = "Randomly assign dishes"


class DiningParticipationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'dining_list', "work_groceries", "work_cook", "work_dishes", "paid")
    list_filter = ('user', 'dining_list__relevant_date', "work_groceries", "work_cook", "work_dishes", "paid")

    fieldsets = (
        ("Relaties", {
            'fields': ('user', 'dining_list')
        }),
        ('Werk', {
            'fields': ('work_groceries', 'work_cook', 'work_dishes', "paid")
        })
    )


class DiningStatsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_helped', 'total_participated')

    search_fields = ('user__username', 'user__first_name', "user__last_name")

    fieldsets = (
        ('Relaties', {
            'fields': ('user',)
        }),
        ('Stats', {
            'fields': ('total_participated', 'total_helped')
        })
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "body")


class SpecialDateModelAdmin(admin.ModelAdmin):
    list_display = ("date_implied", "date_is_registerable", "message", "date_created")
    list_filter = ("date_implied", "date_is_registerable", "date_created")
    list_filter = ("date_implied", "date_is_registerable", "date_created")

admin.site.register(DiningList, DiningListAdmin)
admin.site.register(DiningParticipation, DiningParticipationAdmin)
admin.site.register(DiningStats, DiningStatsAdmin)
admin.site.register(DiningParticipationThird)
admin.site.register(DiningComment, CommentAdmin)
admin.site.register(RecipeModel)
admin.site.register(SpecialDateModel, SpecialDateModelAdmin)
