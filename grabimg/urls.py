from django.conf.urls import patterns, url

from grabimg import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^getsoup/$', views.getsoup, name='getsoup'),
)
