from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^extrainfo/(?P<country_name>[\w]+)/$', views.extrainfo, name='extrainfo')

]