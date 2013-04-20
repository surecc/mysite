from django.conf.urls import patterns, url

from extractor import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^showpic/$', views.showpic, name='showpic'),
)
