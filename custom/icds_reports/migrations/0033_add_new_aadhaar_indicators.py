# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-23 22:40
from __future__ import unicode_literals

from __future__ import absolute_import
from django.db import migrations

from corehq.sql_db.operations import RawSQLMigration

migrator = RawSQLMigration(('custom', 'icds_reports', 'migrations', 'sql_templates'))


class Migration(migrations.Migration):

    dependencies = [
        ('icds_reports', '0032_create_datasource_views'),
    ]

    operations = [
        migrator.get_migration('update_tables16.sql'),
    ]
