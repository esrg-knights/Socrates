from django.contrib import admin

# Register your models here.
from news.models import Post


class NewsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "date_posted")
    fields = ('title', 'body')
    actions = ['make_published',]

    def make_published(modeladmin, request, queryset):
        for item in queryset:
            item.publish()
    make_published.short_description = "Publish posts to users"

admin.site.register(Post, NewsAdmin)