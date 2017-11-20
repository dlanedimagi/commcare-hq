# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-09 07:09
from __future__ import unicode_literals

from __future__ import absolute_import
from django.db import migrations

from corehq.util.django_migrations import AlterIndexIfNotExists


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0008_increase_name_max_length'),
    ]

    operations = [
        AlterIndexIfNotExists(
            name='sqllocation',
            index_together=set([('tree_id', 'lft', 'rght')]),
        ),
    ]
