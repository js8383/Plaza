# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-14 22:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plaza', '0011_assignment_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='team_name',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='person',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='person', to=settings.AUTH_USER_MODEL),
        ),
    ]
