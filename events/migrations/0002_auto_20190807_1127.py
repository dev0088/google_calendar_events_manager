# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-08-07 11:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='override',
            name='reminder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='overriders', to='events.Reminder'),
        ),
    ]