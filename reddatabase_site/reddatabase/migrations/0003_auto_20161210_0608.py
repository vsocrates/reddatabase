# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-10 06:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reddatabase', '0002_auto_20161209_2302'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment_hasa_submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cid', models.CharField(max_length=6)),
                ('postid', models.CharField(max_length=6)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='comment_hasa_submission',
            unique_together=set([('cid', 'postid')]),
        ),
    ]
