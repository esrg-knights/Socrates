from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class DetailsModel(models.Model):
    related_user = models.ForeignKey(User)

    straat = models.CharField(max_length=255)
    woonplaats = models.CharField(max_length=255)
    postcode = models.CharField(max_length=10)

    telefoonnummer = models.CharField(max_length=20)
    geboortedatum = models.DateField()

    instituut = models.CharField(max_length=5, choices=(
        ('TUE', "Technische Universiteit Eindhoven"),
        ('FON', "Fontys Eindhoven"),
        ("BE", "Universiteit of Hogeschool buiten Eindhoven"),
        ("NIET", "Niet")
    ))

    kaartnummer = models.CharField(max_length=20, blank=True, null=True)
