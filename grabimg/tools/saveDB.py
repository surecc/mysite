#coding=utf-8
'''
Created on Apr. 16, 2013

@author: surecc
'''
#grab the Taobao: title|price|url|img
from mysite.models import Cate1, Cate2, Commidity, Feature, Imagedata

'''
 if cid == -1 : need to find the category by name
 if catename not in db, then create it
'''
def saveToCommidity(price, desc, url):
	com = Commidity.objects.create(price=price, desc=desc, url=url)

def saveToImagedata(cid, price, desc, url, localfile, gender):
	cate = Cate2.objects.filter(id=cid)
	com = Commidity.objects.create(price=price, desc=desc, url=url)
	com.save()
	feature = Feature.objects.create()
	#save to imagedata
	data = Imagedata.objects.create(category_id=cid, commidity=com, feature=feature, localfile=localfile, gender=gender)
	#data = Imagedata.objects.create(cate2=cate,commidity=com,feature=feature,localfile=localfile,gender=gender)
	data.save()
	return data.id
