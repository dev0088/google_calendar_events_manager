# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-09-03 21:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('senders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Oauth2Token',
            fields=[
                ('sender', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='sender_oauth2token', serialize=False, to='senders.Sender')),
                ('access_token', models.CharField(max_length=254)),
                ('refresh_token', models.CharField(max_length=254)),
                ('token_expiry', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'SenderOauth2Token',
                'verbose_name_plural': 'SenderOauth2Tokens',
                'ordering': ('sender', 'updated_at'),
                'managed': True,
            },
        ),
        migrations.AlterUniqueTogether(
            name='oauth2token',
            unique_together=set([('sender',)]),
        ),
    ]
