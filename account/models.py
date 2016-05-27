import uuid
from signal import signal

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import models


# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class DetailsModel(models.Model):
    related_user = models.OneToOneField(User)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    straat = models.CharField(max_length=255, null=True, blank=True, help_text="Straat van je adres")
    woonplaats = models.CharField(max_length=255, null=True, blank=True, help_text="Waar je woont")
    postcode = models.CharField(max_length=10, null=True, blank=True, help_text="Je postcode")

    telefoonnummer = models.CharField(max_length=20, null=True, blank=True,
                                      help_text="Mobiel telefoonnummer waarop we je kunnen bereiken")
    geboortedatum = models.DateField(null=True, blank=True, help_text="Formaat is DD-MM-YYYY")

    instituut = models.CharField(max_length=5, choices=(
        ('TUE', "Technische Universiteit Eindhoven"),
        ('FON', "Fontys Eindhoven"),
        ("BE", "Universiteit of Hogeschool buiten Eindhoven"),
        ("NIET", "Niet")
    ), default='TUE', help_text="Bij welk instituut studeer je?")

    kaartnummer = models.CharField(max_length=20, blank=True, null=True,
                                   help_text="Het kaartnummer van je TU-pas. Vul dit enkel in als je op de TUE zit")

    allergies = models.TextField(
        help_text="Allergieen van de eetlijst.", null=True,
        blank=True)
    rather_nots = models.TextField(
        verbose_name="Haal me van de eet-lijst",
        help_text="Als een van deze items gebruikt wordt bij het koken, wil je van de eetlijst afgehaald worden."
                  "Door het invullen van dit veld verga je het recht op eten. De kok kan jou er dus zomaar af halen.",
        null=True, blank=True)

    nickname = models.CharField(help_text="this is stupid. max 50 characters.", max_length=50, null=True, blank=True)

    show_nicknames = models.BooleanField(help_text="Zie de nicknames van jezelf en andere gebruikers waar mogelijk",
                                         default=True)

    theme = models.SmallIntegerField(choices=(
        (1, "Material"),
        (2, "FRIEND COMPUTER MODE"),
        (3, "None (Why would you want this?!)"),
        (4, 'Knigts (WIP)'),
    ), default=1, help_text="Thema van de UI. Alleen Material wordt officieel ondersteund")

    is_softbanned = models.BooleanField(default=False)
    ban_reason = models.CharField(max_length=50, default="")

    def nickname_is_image(self):
        return self.nickname.endswith(".jpg") or self.nickname.endswith(".png") or self.nickname.endswith(".gif")

    @receiver(post_save, sender=User)
    def create_new(sender, instance=None, created=False, **kwargs):
        if created:
            DetailsModel.objects.get_or_create(related_user=instance)

class PasswordChangeRequestModel(models.Model):
    user = models.ForeignKey(User)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def send_change_mail(self):
        send_mail("Wachtwoord veranderen",
                  "https://app.kotkt.nl{}".format(reverse("account:change_password_complete", args=[self.token, ])),
                  "watson@kotkt.nl", [self.user.email, ])
