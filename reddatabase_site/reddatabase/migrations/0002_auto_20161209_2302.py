# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-10 04:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reddatabase', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='username',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='subredditName',
        ),
    ]