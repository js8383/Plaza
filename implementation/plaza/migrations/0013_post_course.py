# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-15 16:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plaza', '0012_auto_20160414_2240'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='course',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='plaza.Course'),
            preserve_default=False,
        ),
    ]
