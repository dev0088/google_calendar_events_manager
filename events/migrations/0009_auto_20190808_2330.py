# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-08-08 23:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20190808_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reminder',
            name='event',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='reminder', serialize=False, to='events.Event'),
        ),
    ]
