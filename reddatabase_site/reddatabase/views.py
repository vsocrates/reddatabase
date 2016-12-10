from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def index(request):
	template = loader.get_template('reddatabase/index.html')
	context = {}
	return HttpResponse(template.render(context, request))

def number_moderators(self):
	with connection.cursor() as cursor:
		cursor.execute("SELECT COUNT(*) FROM reddatabase_user U, subreddit_hasa_user S WHERE U.username = S.username AND S.subredditName = countryName")
		rows = cursor.namedtuplefetchall()
	return rows

# Create your views here.i
