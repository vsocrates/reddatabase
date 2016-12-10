from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from django.db import connection

def index(request):
	#num_mods = number_moderators()
	template = loader.get_template('reddatabase/index.html')
	context = {}#= {'num_mods':num_mods}
	return HttpResponse(template.render(context, request))

def number_moderators():
	with connection.cursor() as cursor:
		cursor.execute("SELECT COUNT(*) FROM reddatabase_user U, subreddit_hasa_user S WHERE U.username = S.username AND S.subredditName = Canada")
		rows = cursor.namedtuplefetchall()
	return rows

# Create your views here.i
