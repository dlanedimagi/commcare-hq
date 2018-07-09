# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-09 18:33
from __future__ import unicode_literals

from datetime import date

from django.db import migrations

from corehq.sql_db.operations import HqRunPython, noop_migration_fn


def assert_date_delay_invoicing_does_not_apply(apps, schema_editor):
    Subscription = apps.get_model('accounting', 'Subscription')
    assert not Subscription.visible_objects.filter(
        date_delay_invoicing__isnull=False,
        date_delay_invoicing__gt=date(2018, 1, 1),
    ).exists()


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0033_auto_20180709_1837'),
    ]

    operations = [
        HqRunPython(assert_date_delay_invoicing_does_not_apply, reverse_code=noop_migration_fn),
        migrations.RemoveField(
            model_name='subscription',
            name='date_delay_invoicing',
        ),
    ]
