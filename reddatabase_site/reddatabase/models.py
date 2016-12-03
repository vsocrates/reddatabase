from __future__ import unicode_literals

from django.db import models

class submission(models.Model):
	postid = models.CharField(max_length=6),(primary_key=True)
	username = models.CharField(max_length=20)
	subredditName = models.CharField(max_length=20)
	title = models.CharField(max_length=300)
	upvotes = models.IntegerField
	downvotes = models.IntegerField
	postType = models.IntegerField
	timeSubmitted = models.DateTimeField

class Comment(models.Model):
	cid = models.CharField(max_length=6)(,primary_key=True)
	p_cid = models.CharField(max_length=6)
	postid = models.CharField(max_length=6)
	text = models.CharFIeld(max_length=40000)
	username = models.CharFIeld(max_length=20)
	score = models.IntegerField
	commentType = models.IntegerField
	timeSubmitted = models.DateTimeField

class moderator(models.Model):
	username = username = models.CharField(max_length=20),(primary_key=True)
	subredditName = models.CharField(max_length=20),(primary_key=True)

class user(models.Model):
	username = models.CharField(max_length=20),(primary_key=True)
	karma = models.IntegerField

class subreddit(models.Model):
	subredditName = models.CharField(max_length=20, primary_key=True)
	subscribers = models.IntegerField()

class linkpost(models.Model):
	postid = models.CharField(max_length=6, primary_key=True)
	url = models.CharField(max_length=10000)

class textpost(models.Model):
	postid = models.CharField(max_length=6, primary_key=True)
	content = models.CharField(max_length=40000)
 your models here.
