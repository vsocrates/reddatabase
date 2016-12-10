from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from django.db import connection
from collections import namedtuple


def index(request):

    template = loader.get_template('reddatabase/index.html')
    context = {}

    return HttpResponse(template.render(context, request))

def extrainfo(request, country_name):

    number_moderators1 =  number_moderators(country_name)
    avg_upvotes1 = avg_upvotes(country_name)
    comments_per_post1 = comments_per_post(country_name)
    activity_over_time1 = activity_over_time(country_name)
    number_linkposts1 = number_linkposts(country_name)
    number_textposts1 = number_textposts(country_name)

    template = loader.get_template('reddatabase/country_page.html')
    context = { 'number_moderators':number_moderators1,
                'avg_upvotes':avg_upvotes1,
                'comments_per_post':comments_per_post1,
                'activity_over_time':activity_over_time1,
                'number_textposts':number_textposts1,
                'number_linkposts':number_linkposts1,
        }

    return HttpResponse(template.render(context, request))

def number_moderators(countryName):
	with connection.cursor() as cursor:
		cursor.execute("SELECT COUNT(*) FROM reddatabase_user U, reddatabase_subreddit_hasa_user S WHERE U.username = S.username AND S.subredditName = '" + countryName + "'")
		rows = cursor.fetchall()
	return rows

def avg_upvotes(countryName):
        with connection.cursor() as cursor:
		cursor.execute("SELECT AVG(P.upvotes) FROM reddatabase_submission P, reddatabase_submission_hasa_subreddit S WHERE P.postid = S.postid AND S.subredditName = '" + countryName + "'")
                rows = cursor.fetchall()
        return rows

def comments_per_post(countryName):
        with connection.cursor() as cursor:
		cursor.execute("SELECT AVG(count) FROM (SELECT COUNT(C) as count FROM reddatabase_comment C, reddatabase_comment_replied_submission S, reddatabase_submission_hasa_subreddit R WHERE S.cid = C.cid AND S.postid = R.postid AND R.subredditName = '" + countryName +  "' GROUP BY S.postid)")
                rows = cursor.fetchall()
        return rows

def activity_over_time(countryName):
	#add in a for loop that populates a list	

	for hourNum in range(0, 24):
		if(hourNum < 9):
			low_hour_string = "0" + str(hourNum)
        		high_hour_string = "0" + str(hourNum + 1)
    		elif(hourNum == 9):
        		low_hour_string = "0" + str(hourNum)
        		high_hour_string = str(hourNum)
    		else:
        		low_hour_string = str(hourNum)
        		high_hour_string = str(hourNum)
    		low_hour = "2016-12-08 " + low_hour_string + ":00:00"
    		high_hour = "2016-12-08 " + high_hour_string + ":00:00"

        	with connection.cursor() as cursor:
			cursor.execute("SELECT COUNT(*) FROM redattabase_submisison_hasa_subreddit R, reddatabase_submission S WHERE R.subredditName = " + countryName + " AND R.postid = S.postid AND S.timeSubmitted >= " + low_hour_string + " AND S.timeSubmitted <" + high_hour_string)
			rows = cursor.fetchall()
			activityLevels.append(rows)
	
	return activityLevels

def number_linkposts(countryName):
        with connection.cursor() as cursor:
		cursor.execute("SELECT COUNT(*) FROM reddatabase_linkpost P, reddatabase_submission_hasa_subreddit S WHERE P.postid = S.postid AND S.subredditName = '" + countryName + "'")
                rows = cursor.fetchall()
        return rows

def number_textposts(countryName):
        with connection.cursor() as cursor:
		cursor.execute("SELECT COUNT(*) FROM reddatabase_textpost P, reddatabase_submission_hasa_subreddit S WHERE P.postid = S.postid AND S.subredditName = '" + countryName + "'")
                rows = cursor.fetchall()
        return rows
# Create your views here.i
