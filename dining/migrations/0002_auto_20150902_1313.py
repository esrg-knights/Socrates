# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        ('dining', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dininglist',
            name='owner',
            field=models.ForeignKey(related_name='owned_by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
