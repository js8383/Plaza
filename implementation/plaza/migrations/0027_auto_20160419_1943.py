# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-19 19:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plaza', '0026_auto_20160419_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='parent_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='root_id',
            field=models.IntegerField(default=0),
        ),
    ]
