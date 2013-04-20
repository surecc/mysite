# Create your views here.
from django.shortcuts import render_to_response
from django.http import  HttpResponse, HttpResponseRedirect
from grabimg.forms import SoupForm
from mysite.models import *
# tool functions
from grabimg.tools import getRandom, getHtml, getResource, taobao_lib, saveImg
# get conf 
from django.conf import settings

def getsoup_old(request):
    return HttpResponse('i will think about it. i mean get soup.')

def show_soup_result(request):
    return HttpResponse('i have already done! Thanks!')

import re
import time
import os.path
import json
#from grabimg.conf import surecc
def getsoup(request):
    if request.method == 'POST':
        form = SoupForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            # as below, will grab the data of the url
            url = clean_data['url']
            print url
            website = '360buy'
            cate = clean_data['cate']
            # store the url into a file named try.txt
            #rd = getRandomStr(10)
            #rd = getRandom.getRandomStr(10)
            rd = getRandom.getUUID()
            #path_img = os.path.join(settings.GRAB_IMG_ROOT, rd)
            # os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
            #path_img = os.path.join(os.path.join(os.path.dirname(__file__)), '..\\imgdb\\taobao_' + rd + '.jpg')
            #localfile = os.path.join(os.path.join(os.path.dirname(__file__)), '..\\imgdb\\url_' + rd + '.txt')
            #getHtml.grabHref(url, localfile)
            #getResource.grabHref(url, localfile)
            #getResource.grab_360buy(url, localfile)
            #getResource.grab_360buy_saveToModel(url, 1, 1, localfile)
            if website == 'taobao':
                getResource.grabHref(url, localfile)
                data = taobao_lib.get_json(url)
                json_data = json.loads(data)
                json.loads(data, None)
                json_item_list = json_data['itemList']
                for item in json_item_list:
                    price = item['currentPrice']
                    name = item['fullTitle']
                    url = item['storeLink']
                    img_url = item['image']
                    #save img
                    saveImg.saveImg(img_url, path_img)
            elif website == '360buy':
		#debug
		print settings.MEDIA_ROOT	
		target_dir = settings.MEDIA_ROOT + 'jd360/'
		img_root = target_dir + time.strftime('%Y%m%d')
		#now = time.strftime('%H%M%S')
		if not os.path.exists(img_root):
			os.mkdir(img_root) # make directory
	        # img_root = os.path.join(settings.MEDIA_ROOT, 'jd360/') 
		#create the path
		#os.mkdir(img_root)
                # getResource.grab_360buy(url, img_root)
		#row = re.findall("\w+",url);
		
		#for url_li in row:
		#	print 'url_li:???????????'+url_li
		getResource.grab_360buy_bag_m(url, img_root)
		print 'img_root-----------'
		print img_root
                #print name + price + url + img_url
            return render_to_response('beautiful_soup.html',{'form': form, 'ans':img_root})
    else:
        form = SoupForm(initial={'url':'http://list.jd.com/1672-2576-5262.html'})
    return render_to_response('beautiful_soup.html',{'form': form})


def index(request):
        return HttpResponse("Hello, This is grabimg index page!")

