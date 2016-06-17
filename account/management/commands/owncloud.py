from django.core.mail import send_mail

import account.management.lowncloud as owncloud
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

from django.conf import settings


class Command(BaseCommand):
    help = 'Does some magical work'

    def handle(self, *args, **options):
        """ Do your work here """
        users = User.objects.all()
        groups = Group.objects.all()

        oc = owncloud.Client("https://kotkt.nl/cloud/owncloud")

        oc.login(settings.OWNCLOUD_USER, settings.OWNCLOUD_PW)

        for user in users:
            try:
                pw = generate_temp_password(10)
                oc.create_user(user.username, pw)
                print("User {0} has password {1}".format(user.username, pw))

                send_mail(
                    "Je hebt een account gekregen op owncloud!",
                    "Je gebruikersnaam is {0} en je wachtwoord is {1} . Verander dit AUB zo snel mogelijk, aangezien het wachtwoord is verstuurd in plaintext! Owncloud is te vinden op https://kotkt.nl/cloud/owncloud/".format(user.username, pw),
                    "app@kotkt.nl",
                    [user.email,]
                )
            except owncloud.OCSResponseError:
                print("User {} already exists".format(user))

        for group in groups:
            try:
                oc.create_group(group.name)
            except owncloud.OCSResponseError:
                print("Group {} already exists".format(group))

            for user in group.user_set.all():
                try:
                    oc.add_user_to_group(user.username, group.name)
                except:
                    print("User {} is already in group".format(user))

        print("There are {} users".format(users.count()))
        print("There are {} groups".format(groups.count()))


def generate_temp_password(length):
    if not isinstance(length, int) or length < 8:
        raise ValueError("temp password must have positive length")

    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789abcdefghijklmnopqrstuvwxyz"
    from os import urandom
    return "".join([chars[ord(c) % len(chars)] for c in urandom(length)])
