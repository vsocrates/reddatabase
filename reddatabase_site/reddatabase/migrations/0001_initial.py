# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-10 02:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('cid', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('p_cid', models.CharField(max_length=6)),
                ('postid', models.CharField(max_length=6)),
                ('text', models.CharField(max_length=40000)),
                ('username', models.CharField(max_length=20)),
                ('score', models.IntegerField()),
                ('commentType', models.IntegerField()),
                ('timeSubmitted', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Comment_hasa_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cid', models.CharField(max_length=6)),
                ('username', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='linkpost',
            fields=[
                ('postid', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('url', models.CharField(max_length=10000)),
            ],
        ),
        migrations.CreateModel(
            name='submission',
            fields=[
                ('postid', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=20)),
                ('subredditName', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=300)),
                ('upvotes', models.IntegerField()),
                ('downvotes', models.IntegerField()),
                ('postType', models.IntegerField()),
                ('timeSubmitted', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='submission_hasa_subreddit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postid', models.CharField(max_length=6)),
                ('subredditName', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='subreddit',
            fields=[
                ('subredditName', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('subscribers', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='subreddit_hasa_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subredditName', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='textpost',
            fields=[
                ('postid', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=40000)),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('username', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('karma', models.IntegerField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='subreddit_hasa_user',
            unique_together=set([('subredditName', 'username')]),
        ),
        migrations.AlterUniqueTogether(
            name='submission_hasa_subreddit',
            unique_together=set([('postid', 'subredditName')]),
        ),
        migrations.AlterUniqueTogether(
            name='comment_hasa_user',
            unique_together=set([('cid', 'username')]),
        ),
    ]
