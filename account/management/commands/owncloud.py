from django.core.mail import send_mail

import account.management.lowncloud as owncloud
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

from django.conf import settings

"""
Syncs django users and groups to owncloud. Generates passwords for new users
Usage: python manage.py owncloud
"""


class Command(BaseCommand):
    help = 'Syncs django users to owncloud'

    def handle(self, *args, **options):
        """ Do your work here """
        django_users = User.objects.all()
        django_groups = Group.objects.all()

        oc = owncloud.Client("https://kotkt.nl/cloud/owncloud")

        oc.login(settings.OWNCLOUD_USER, settings.OWNCLOUD_PW)

        # Create users
        for user in django_users:
            if not oc.user_exists(user.username):
                pw = generate_temp_password(10)
                oc.create_user(user.username, pw)
                print("User {0} has password {1}".format(user.username, pw))

                # Send mail with password
                send_mail(
                    "Je hebt een account gekregen op owncloud!",
                    "Je gebruikersnaam is {0} en je wachtwoord is {1} . Verander dit AUB zo snel mogelijk, aangezien het wachtwoord is verstuurd in plaintext! Owncloud is te vinden op https://kotkt.nl/cloud/owncloud/".format(
                        user.username, pw),
                    "app@kotkt.nl",
                    [user.email, ]
                )

        # Create groups
        for group in django_groups:
            if not oc.group_exists(group.name):
                oc.create_group(group.name)

        for user in django_users:
            oc_groups = oc.get_user_groups(user.username)
            user_groups = [str(x.name) for x in user.groups.all()]

            # If no groups, purge all
            if len(user_groups) == 0:
                for group in oc_groups:
                    oc.remove_user_from_group(user.username, group)
            else:
                for group in user_groups:
                    if group not in oc_groups:
                        print("adding {0} to {1}".format(user.username, group))
                        oc.add_user_to_group(user.username, group)

                for group in oc_groups:
                    if group not in user_groups:
                        print("removing {0} from {1}".format(user.username, group))
                        oc.remove_user_from_group(user.username, group)

        print("There are {} users".format(django_users.count()))
        print("There are {} groups".format(django_groups.count()))


def generate_temp_password(length):
    if not isinstance(length, int) or length < 8:
        raise ValueError("temp password must have positive length")

    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789abcdefghijklmnopqrstuvwxyz"
    from os import urandom
    return "".join([chars[ord(c) % len(chars)] for c in urandom(length)])
