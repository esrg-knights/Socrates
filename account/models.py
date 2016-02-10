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
    geboortedatum = models.DateField(null=True, help_text="Formaat is DD-MM-YYYY")

    instituut = models.CharField(max_length=5, choices=(
        ('TUE', "Technische Universiteit Eindhoven"),
        ('FON', "Fontys Eindhoven"),
        ("BE", "Universiteit of Hogeschool buiten Eindhoven"),
        ("NIET", "Niet")
    ), default='TUE')

    kaartnummer = models.CharField(max_length=20, blank=True, null=True)

    allergies = models.TextField(help_text="Dingen waarvoor je allergies bent. Zet hier AUB alleen maar serieuze dingen bij.", null=True, blank=True)
    rather_nots = models.TextField(help_text="Dingen die je liever niet wil eten.", null=True, blank=True)
    nickname = models.CharField(help_text="this is stupid. max 50 characters.", max_length=50, null=True, blank=True)