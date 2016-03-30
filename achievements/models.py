from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from slugify import slugify


# Create your models here.
class Game(models.Model):
    name = models.CharField(100)


class Achievement(models.Model):
    name = models.CharField(max_length=50, help_text="Naam van de achievement")
    name_slug = models.CharField(max_length=50, null=True, blank=True, help_text="slug van de naam. Vul dit niet in")

    related_game = models.ForeignKey(Game, help_text="Spel waar de achievement bij hoort")

    description = models.TextField(help_text="Beschrijving van de achievements")

    date_created = models.DateTimeField(auto_now=True, help_text="datum aangemaakt")
    date_last_accessed = models.DateTimeField(help_text="Datum waarop de achievement voor het laatst verander was")

    def save(self, *args, **kwargs):
        self.date_last_accessed = timezone.now()
        self.name_slug = slugify(self.name)
        super(Achievement, self).save(*args, **kwargs)

    def get(self):
        return AchievementGet.objects.filter(achievement=self)

    def __str__(self):
        return self.name.__str__()

    def __unicode__(self):
        return self.name


class AchievementGet(models.Model):
    user = models.ForeignKey(User, related_name="user", help_text="Gebruiker die een Achievement heeft gehaald")
    achievement = models.ForeignKey(Achievement, help_text="Achievement die is gehaald")
    awarded_by = models.ForeignKey(User, related_name="awarded_by",
                                   help_text="Lid van de ZG die de achievement heeft uitgedeeld")

    date_achieved = models.DateTimeField(auto_now=True, help_text="datum aangemaakt")

    score = models.IntegerField(help_text="Score die is gehaald voor de achievement")

    class Meta:
        ordering = ("-score",)
