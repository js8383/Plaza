# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-20 16:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plaza', '0031_auto_20160420_0834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications_received', to='plaza.Person'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications_sent', to='plaza.Person'),
        ),
    ]
