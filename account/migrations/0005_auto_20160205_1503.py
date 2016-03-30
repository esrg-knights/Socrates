# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-05 15:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20150817_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailsmodel',
            name='allergies',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='detailsmodel',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='detailsmodel',
            name='geboortedatum',
            field=models.DateField(help_text='Formaat is DD-MM-YYYY', null=True),
        ),
        migrations.AlterField(
            model_name='detailsmodel',
            name='instituut',
            field=models.CharField(choices=[('TUE', 'Technische Universiteit Eindhoven'), ('FON', 'Fontys Eindhoven'), ('BE', 'Universiteit of Hogeschool buiten Eindhoven'), ('NIET', 'Niet')], default='TUE', max_length=5),
        ),
        migrations.AlterField(
            model_name='detailsmodel',
            name='postcode',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='detailsmodel',
            name='related_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='detailsmodel',
            name='straat',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='detailsmodel',
            name='telefoonnummer',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='detailsmodel',
            name='woonplaats',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
