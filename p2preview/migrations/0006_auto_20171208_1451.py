# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-08 09:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p2preview', '0005_auto_20171208_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(default='', max_length=254, unique=True),
        ),
    ]
