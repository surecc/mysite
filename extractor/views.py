# Create your views here.
from django.shortcuts import render_to_response
from django.http import  HttpResponse, HttpResponseRedirect
from extractor.tools import FeatureExtractor

def index(request):
        return HttpResponse("Hello, This is extractor index page!")

def showpic(request):
	return HttpResponse("I will show you pictures, don't worry!")
