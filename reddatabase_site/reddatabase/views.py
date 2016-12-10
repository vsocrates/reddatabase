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
		cursor.execute("SELECT COUNT(*) FROM reddatabase_user U, reddatabase_subreddit_hasa_user S WHERE U.username = S.username AND S.subredditName = 'sweden'")
		rows = cursor.fetchall()
	return rows

# Create your views here.i
