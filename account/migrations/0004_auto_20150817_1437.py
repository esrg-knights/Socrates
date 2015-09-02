# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('account', '0003_auto_20150817_1423'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detailsmodel',
            old_name='birthday',
            new_name='geboortedatum',
        ),
        migrations.RemoveField(
            model_name='detailsmodel',
            name='adress',
        ),
        migrations.AddField(
            model_name='detailsmodel',
            name='instituut',
            field=models.CharField(default='FON', max_length=5, choices=[(b'TUE', b'Technische Universiteit Eindhoven'),
                                                                         (b'FON', b'Fontys Eindhoven'), (b'BE',
                                                                                                         b'Universiteit of Hogeschool buiten Eindhoven'),
                                                                         (b'NIET', b'Niet')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detailsmodel',
            name='kaartnummer',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='detailsmodel',
            name='postcode',
            field=models.CharField(default='5623 GX', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detailsmodel',
            name='straat',
            field=models.CharField(default='Generaal Bentinckstraat 48', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detailsmodel',
            name='telefoonnummer',
            field=models.CharField(default='06 38 21 23 27', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detailsmodel',
            name='woonplaats',
            field=models.CharField(default='Eindhoven', max_length=255),
            preserve_default=False,
        ),
    ]
