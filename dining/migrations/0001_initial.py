# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DiningList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('relevant_date', models.DateField(auto_now=True, auto_created=True)),
                ('owner', models.ForeignKey(related_name='owned_by', to=settings.AUTH_USER_MODEL)),
                ('started_by', models.ForeignKey(related_name='started_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DiningParticipation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('work_dishes', models.BooleanField(default=False)),
                ('work_cook', models.BooleanField(default=False)),
                ('work_groceries', models.BooleanField(default=False)),
                ('dining_list', models.ForeignKey(to='dining.DiningList')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DiningStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_participated', models.IntegerField(default=0)),
                ('total_helped', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
