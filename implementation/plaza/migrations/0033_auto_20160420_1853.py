# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-20 18:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plaza', '0032_auto_20160420_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='assignee',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
