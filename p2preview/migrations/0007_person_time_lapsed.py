# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-08-20 12:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p2preview', '0006_auto_20180820_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='time_lapsed',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
    ]
