# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('account', '0002_detailsmodel_adres'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detailsmodel',
            old_name='adres',
            new_name='adress',
        ),
        migrations.AlterField(
            model_name='detailsmodel',
            name='birthday',
            field=models.DateField(),
        ),
    ]
