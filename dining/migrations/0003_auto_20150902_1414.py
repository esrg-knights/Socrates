# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('dining', '0002_auto_20150902_1313'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dininglist',
            name='started_by',
        ),
        migrations.AddField(
            model_name='diningparticipation',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
