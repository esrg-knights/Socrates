# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-05 15:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dining', '0003_auto_20150902_1414'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiningParticipationThird',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('paid', models.BooleanField(default=False)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelOptions(
            name='diningparticipation',
            options={'ordering': ('user__first_name',)},
        ),
        migrations.AddField(
            model_name='dininglist',
            name='closing_time',
            field=models.TimeField(default='14:00'),
        ),
        migrations.AlterField(
            model_name='dininglist',
            name='relevant_date',
            field=models.DateField(),
        ),
        migrations.AddField(
            model_name='diningparticipationthird',
            name='dining_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dining.DiningList'),
        ),
    ]
