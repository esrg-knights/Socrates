import uuid

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
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

    allergies = models.TextField(
            help_text="Dingen waarvoor je allergies bent. Zet hier AUB alleen maar serieuze dingen bij.", null=True,
            blank=True)
    rather_nots = models.TextField(help_text="Dingen die je liever niet wil eten.", null=True, blank=True)
    nickname = models.CharField(help_text="this is stupid. max 50 characters.", max_length=50, null=True, blank=True)

    def nickname_is_image(self):
        return self.nickname.endswith(".jpg") or self.nickname.endswith(".png") or self.nickname.endswith(".gif")


class PasswordChangeRequestModel(models.Model):
    user = models.ForeignKey(User)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def send_change_mail(self):
        send_mail("Wachtwoord veranderen",
                  "https://app.kotkt.nl{}".format(reverse("account:change_password_complete", args=[self.token, ])),
                  "watson@kotkt.nl", [self.user.email, ])
