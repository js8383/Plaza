# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-19 02:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plaza', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='parent_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='plaza.Post'),
        ),
    ]
