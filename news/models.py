from django.db import models

# Create your models here.
from django.utils.datetime_safe import datetime
from slugify import slugify


class Post(models.Model):
    title = models.CharField(max_length=300)
    title_slug = models.CharField(max_length=300, null=True, blank=True)

    date_posted = models.DateTimeField(auto_created=True)
    date_last_edited = models.DateTimeField(null=True, blank=True)

    body = models.TextField(help_text="Markdown is enabled")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.title_slug = slugify(self.title)
        self.date_last_edited = datetime.now()

        super(Post, self).save(force_insert, force_update, using, update_fields)

    class Meta():
        ordering = ("-date_posted", "-date_last_edited")
