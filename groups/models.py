from __future__ import unicode_literals
from django.contrib.auth.models import Group

from django.db import models

# Create your models here.
class GroupDetails(models.Model):
    related_user = models.OneToOneField(Group)
    category = models.SmallIntegerField(choices=(
        (1, "Commissie"),
        (2, "Orde"),
        (3, "Werkgroep"),
        (4, "Campaign"),
        (5, "-")
    ), default=5, help_text="Het type groep")

    name = models.CharField(max_length=50)
    shorthand = models.CharField(max_length=10)
    description = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return self.name

