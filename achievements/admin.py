from django.contrib import admin
from .models import *
# Register your models here.

class AchievementAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "priority")
    list_filter = ("date_last_accessed", "isPublic")

class AchievementGetAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "achievement", "awarded_by", "score")
    list_filter = ("user", "achievement", "awarded_by")

admin.site.register(Game)
admin.site.register(Achievement, AchievementAdmin)
admin.site.register(AchievementGet, AchievementGetAdmin)