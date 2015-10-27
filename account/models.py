import uuid

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class DetailsModel(models.Model):
    related_user = models.OneToOneField(User)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    straat = models.CharField(max_length=255, null=True)
    woonplaats = models.CharField(max_length=255, null=True)
    postcode = models.CharField(max_length=10, null=True)

    telefoonnummer = models.CharField(max_length=20, null=True)
    geboortedatum = models.DateField(null=True)

    instituut = models.CharField(max_length=5, choices=(
        ('TUE', "Technische Universiteit Eindhoven"),
        ('FON', "Fontys Eindhoven"),
        ("BE", "Universiteit of Hogeschool buiten Eindhoven"),
        ("NIET", "Niet")
    ), default='TUE')

    kaartnummer = models.CharField(max_length=20, blank=True, null=True)