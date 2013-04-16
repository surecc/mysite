# -*- coding:gb18030 -*-
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
import datetime


def hello(request):
	return HttpResponse("Hello World!")

def current_datetime(request):
	now = datetime.datetime.now()
	html = "<html><body>It is now %s</body></html>" % now
	return HttpResponse(html)
def current_datetimeTpl(request):
	now = datetime.datetime.now()
	return render_to_response('current_datetime.html', {'current_datetime': now})
	
def hours_ahead(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
	dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
	html = "<html><body>%s 小时后，将会是： %s</body></html>" % (offset, dt)
	return HttpResponse(html)
