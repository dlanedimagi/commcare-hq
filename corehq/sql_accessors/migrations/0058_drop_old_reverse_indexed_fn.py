# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-30 18:39
from __future__ import absolute_import
from __future__ import unicode_literals

from django.db import migrations

from corehq.sql_db.operations import HqRunSQL


class Migration(migrations.Migration):

    dependencies = [
        ('sql_accessors', '0057_filter_get_reverse_indexed_cases'),
    ]

    operations = [
        HqRunSQL("DROP FUNCTION IF EXISTS get_reverse_indexed_cases(TEXT, TEXT[]);"),
    ]
