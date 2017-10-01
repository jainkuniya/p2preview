# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-01 06:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p2preview', '0007_auto_20171001_0648'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericoption',
            name='optionNo',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='genericoption',
            unique_together=set([('genericId', 'optionNo')]),
        ),
        migrations.AlterUniqueTogether(
            name='groupdetail',
            unique_together=set([('groupId', 'sId')]),
        ),
    ]
