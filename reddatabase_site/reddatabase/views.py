from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from django.db import connection
from collections import namedtuple

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def index(request):
	num_mods = number_moderators()
	template = loader.get_template('reddatabase/index.html')
	context = {'num_mods':num_mods}
	return HttpResponse(template.render(context, request))

def number_moderators():
	with connection.cursor() as cursor:
		cursor.execute("SELECT COUNT(*) FROM reddatabase_user U, reddatabase_subreddit_hasa_user S WHERE U.username = S.username AND S.subredditName = " + countryName)
		rows = cursor.fetchall()
	return rows

def avg_upvotes():
        with connection.cursor() as cursor:
		cursor.execute("SELECT AVG(P.upvotes) FROM reddatabase_submission P, reddatabase_submission_hasa_subreddit S WHERE P.postid = S.postid AND S.subredditName = " + countryName)
                rows = cursor.fetchall()
        return rows

def comments_per_post():
        with connection.cursor() as cursor:
		cursor.execute("SELECT AVG(count) FROM (SELECT COUNT(C) as count FROM reddatabase_comment C, reddatabase_comment_replied_submission S, reddatabase_submission_hasa_subreddit R WHERE S.cid = C.cid AND S.postid = R.postid AND R.subredditName = " + countryName +  "GROUP BY S.postid)")
                rows = cursor.fetchall()
        return rows

def activity_during_hour(low_hour, high_hour):
	#add in a for loop that populates a list
        with connection.cursor() as cursor:
		cursor.execute("SELECT COUNT(*) FROM redattabase_submisison_hasa_subreddit R, reddatabase_submission S WHERE R.subredditName = countryName AND R.postid = S.postid AND S.timeSubmitted >= low_hour AND S.timeSubmitted < high_hour")
                rows = cursor.fetchall()
        return rows

def number_linkposts():
        with connection.cursor() as cursor:
		cursor.execute("SELECT COUNT(*) FROM reddatabase_linkpost P, reddatabase_submission_hasa_subreddit S WHERE P.postid = S.postid AND S.subredditName = countryName")
                rows = cursor.fetchall()
        return rows

def number_textposts():
        with connection.cursor() as cursor:
		cursor.execute("SELECT COUNT(*) FROM reddatabase_textpost P, reddatabase_submission_hasa_subreddit S WHERE P.postid = S.postid AND S.subredditName = countryName")
                rows = cursor.fetchall()
        return rows
# Create your views here.i
