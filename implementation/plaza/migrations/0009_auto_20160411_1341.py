# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-11 13:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plaza', '0008_auto_20160407_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
    ]