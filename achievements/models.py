from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from slugify import slugify


# Create your models here.
class Achievement(models.Model):
    name = models.CharField(max_length=50)
    name_slug = models.CharField(max_length=50, null=True, blank=True)

    related_image = models.FileField(upload_to="media/%y/%m/%d")

    description = models.CharField(max_length=256)

    date_created = models.DateTimeField(auto_now=True)
    date_last_accessed = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.date_last_accessed = timezone.now()
        self.name_slug = slugify(self.name)
        super(Achievement, self).save(*args, **kwargs)

    def get(self):
        return AchievementGet.objects.filter(achievement=self)


class AchievementGet(models.Model):
    user = models.ForeignKey(User, related_name="user")
    achievement = models.ForeignKey(Achievement)
    awarded_by = models.ForeignKey(User, related_name="awarded_by")

    date_achieved = models.DateTimeField(auto_now=True)

    score = models.IntegerField()

    class Meta:
        ordering = ("-score",)
