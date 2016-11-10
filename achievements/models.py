from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from slugify import slugify


# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length=100)
    image = models.FileField(blank=True, null=True, upload_to="%y/%M/%d")

    def __str__(self):
        return self.name.__str__()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class Achievement(models.Model):
    name = models.CharField(max_length=50, help_text="Naam van de achievement")
    name_slug = models.CharField(max_length=50, null=True, blank=True, help_text="slug van de naam. Vul dit niet in")

    related_game = models.ForeignKey(Game, help_text="Spel waar de achievement bij hoort")

    description = models.TextField(help_text="Beschrijving van de achievements")

    priority = models.IntegerField(default=1)

    date_created = models.DateTimeField(auto_now=True, help_text="datum aangemaakt")
    date_last_accessed = models.DateTimeField(help_text="Datum waarop de achievement voor het laatst verander was",
                                              blank=True, null=True)

    image = models.FileField(blank=True, null=True, upload_to="%y/%M%d")

    def save(self, *args, **kwargs):
        self.date_last_accessed = timezone.now()
        self.name_slug = slugify(self.name)
        super(Achievement, self).save(*args, **kwargs)

    def get(self):
        return AchievementGet.objects.filter(achievement=self)[:10]

    def __str__(self):
        return self.name.__str__()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ("-priority", "-date_created",)


class AchievementGet(models.Model):
    user = models.ForeignKey(User, related_name="user", help_text="Gebruiker die een Achievement heeft gehaald")
    achievement = models.ForeignKey(Achievement, related_name="gets", help_text="Achievement die is gehaald")
    awarded_by = models.ForeignKey(User, related_name="awarded_by",
                                   help_text="Lid van de ZG die de achievement heeft uitgedeeld")

    date_achieved = models.DateTimeField(auto_now=True, help_text="datum aangemaakt")

    score = models.IntegerField(help_text="Score die is gehaald voor de achievement", default=-1, null=True, blank=True)

    class Meta:
        ordering = ("-score", "-date_achieved")
