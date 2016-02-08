from django.contrib import admin

# Register your models here.
from news.models import Post


class NewsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "date_posted")
    fields = ('title', 'body')

admin.site.register(Post, NewsAdmin)