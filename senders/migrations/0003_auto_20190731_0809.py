# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-07-31 08:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('senders', '0002_auto_20190731_0650'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='sender',
            unique_together=set([('email',)]),
        ),
    ]
