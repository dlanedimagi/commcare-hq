# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-13 18:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('private_sector_datamigration', '0002_auto_20170512_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adherence',
            name='episodeId',
            field=models.CharField(max_length=8),
        ),
    ]
