# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-08 08:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p2preview', '0004_auto_20171208_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.TextField(blank='True', default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.TextField(default=''),
        ),
    ]