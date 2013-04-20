#coding=utf-8
'''
Created on Jan 16, 2013

@author: surecc
'''
#grab the Taobao: title|price|url|img
from bs4 import BeautifulSoup
import urllib2
import os.path
import sys
from django.conf import settings
# the model of taobao
from mysite import models
from grabimg.tools import saveImg, saveDB
from grabimg.tools import getRandom

# grab the content from an URL
def makeSoup_bad(url):
    try:
        request = urllib2.Request(url=url, headers={'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3' })
        response = urllib2.urlopen(request)
	time.sleep(0.5)
        HTML_response = response.read().decode('gb2312').encode('utf8')
        soup = BeautifulSoup(HTML_response)
    except:
        print 'soup is a mess'
    return soup

def makeSoup(url):
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    return soup

# save info into the models
def saveToModels(model_list):
    return True

def grab_360buy_bag_m(url, localfile):
	soup = makeSoup(url)
	if soup:
		tag_div = soup.find_all('div', id = 'plist')
		if tag_div:
			tag_div_a = tag_div[0].find_all('a', target='_blank')
			#data = []
			i=0
			path_dir = os.path.join(os.path.dirname(localfile))
			print len(tag_div_a)
			for a in tag_div_a:	
				img = a.find('img')
				if not img :
					continue
				print '>>>>>>>>>>>>>>>>>>>>'+str(i)
				url_item = a['href']
				url_img = a.find('img').get('src')
				url_img2 = a.find('img').get('src2')
				desc = a.find('img')['alt']
				#data.append([url_item,url_img,desc])
				if url_img and url_img2:
					continue
				elif not url_img:
					url_img = url_img2
				#print desc
				#print url_item
				#print url_img
				#print img
				#print '----------------------------'
				i += 1
				#img_name = getRandom.getRandomStr(5)
                		path_img = os.path.join(path_dir , str(i) +'.jpg')
				#path_img = os.path.join(path_dir , str(i++) +'.jpg')
				saveImg.saveImg(url_img, path_img)
				#save to db
				#saveDB.saveToImagedata(cid, comid, price, desc, url, localfile, gender)
				saveDB.saveToImagedata(1, 0, desc, url_item, path_img, '1')
	else:
		print "It's empty!!!!! fuque......."
	return True
 
def grab_360buy(url, localfile):
    #print localfile
    soup = makeSoup(url)
    if soup:
        tag_div = soup.find_all('div', id = 'plist')
        if tag_div:
            tag_item_li = tag_div[0].find_all('li')
            #myfile = open(localfile,'w')
            i = 0
            for li in tag_item_li:
                i += 1
                #get the tag of each div
                div = li.find_all('div')
                if div:
                    #print str(i)+'........'
                    p_img = div[0]
                    p_name = div[2]
                    p_price = div[3]
		    # the url of the item
                    #url_img = p_img.img['data-lazyload']
		    #debug
		    print '-------------------------------'
		    print p_img
	            if p_img.img:
					url_img = p_img.img['src']
					url_item = p_img.img['alt']
					path_dir = os.path.join(os.path.dirname(localfile))
					img_name = getRandom.getRandomStr(5)
                    #path_img = os.path.join(path_dir , img_name +'.jpg')
					path_img = os.path.join(path_dir , str(i) +'.jpg')
		    		#debug
					#print url_img
		    		#print path_img
					saveImg.saveImg(url_img, path_img)
                    ##save price
                    #if p_price and p_name and p_img:
                        #url_price = p_price.img['data-lazyload']
                        #path_price = os.path.join(path_dir, img_name+'_price.jpg')
                        #saveImg.saveImg(url_price, path_price)
                        ##get info
                        #myfile.write( str(path_img) + '---')
                        #myfile.write( str(p_name.a.contents) + '---')
                        #myfile.write( str(p_price.img['data-lazyload']) + '---')
                        #myfile.write('\r\n')
                else:
                    print 'it is empty of div.... fuck'
            #myfile.close()
    return True


def grab_360buy_saveToModel(url, id_cate, id_s, localfile):
    request = urllib2.Request(url=url, headers={'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3' })
    response = urllib2.urlopen(request)
    HTML_response = response.read()
    soup = BeautifulSoup(HTML_response,from_encoding="gb18030")

    if soup:
        tag_div = soup.find_all('div', id = 'plist')
        if tag_div:
            tag_item_li = tag_div[0].find_all('li')
            #myfile = open(localfile,'w')
            i = 0
            # get the default
            m_cate = models.Category.objects.get(id=id_cate)
            m_s = models.Seller.objects.get(id=id_s)
            print m_cate
            print type(m_s)
            myfile = open(localfile,'w')
            for li in tag_item_li:
                i += 1
                #get the tag of each div
                div = li.find_all('div')
                if div:
                    print str(i)+'........'
                    p_img = div[0]
                    p_name = div[4]
                    p_price = div[5]
                    #save img
                    url_item = p_img.a['href']
                    url_img = p_img.img['data-lazyload']
                    path_dir = os.path.join(os.path.dirname(localfile))
                    path_img = os.path.join(path_dir , str(i)+'.jpg')
                    saveImg.saveImg(url_img, path_img)
                    ##save price
                    #url_price = p_price.img['data-lazyload']
                    #path_price = os.path.join(path_dir, str(i)+'_price.jpg')
                    #saveImg.saveImg(url_price, path_price)
                    #save to model
                    m_com = models.Commidity(url=url_item, price=0.0, name=str(p_name.a.contents))
                    m_com.categories = m_cate
                    m_com.seller = m_s
                    m_com.save()
                    print m_com
                    m_p = models.Picture(dir=path_dir,commidity=m_com.id)
                    m_p.save()
                    print m_p
                    #get info
                    myfile.write( str(path_img) + '---')
                    myfile.write( str(p_name.a.contents) + '---')
                    myfile.write( str(p_price.img['data-lazyload']) + '---')
                    myfile.write('\r\n')
                else:
                    print 'it is empty of div.... fuck'
            myfile.close()
    return True








       
#grab the urls with user-agent
def grabHref(url, localfile):
    request = urllib2.Request(url=url, 
                              headers={ 
                                       'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3',
                                       'Host' : 'list.taobao.com',
                                       'X-Requested-With' : 'XMLHttpRequest',
                                       'Accept' : 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
                                        })
    response = urllib2.urlopen(request)
    HTML_response = response.read()
    soup = BeautifulSoup(HTML_response)
    if HTML_response:
        myfile = open(localfile,'w')
        myfile.write(HTML_response)
        myfile.close()
    else:
        print 'it is empty here! Shit.............'
        
    '''
    content_li = soup.find_all('li', 'list-item list-item-grid')
    if not content_li:
        print 'it is empty here! Shit.............'
    else:
        myfile = open(localfile,'w')
        m_taobao = models.Commidity()
        list = []
        # get info 
        for item_li in content_li:
            # debug
            print item_li
            #tag_li = item_li.li
            tag_img = item_li.img
            tag_good = item_li.findAll('li', class_ = 'attr-price')
            if tag_good:
                tag_price = tag_good.span.strong.contents
            if tag_img:
                #get the url of the img
                url_download_img = tag_img['src']
                #get url
                m_taobao.url = item_li['data-item']
                m_taobao.name = tag_img['alt']
                m_taobao.price = float(tag_price)
                # for debug
                m_taobao.categories = 0
                m_taobao.sellers = 0
                # debug
                myfile.write(m_taobao)
                #print m_taobao
                # make a list
                list.append(m_taobao)
        myfile.close()
        '''
    return True

#grab the urls of website and save into localfile
def grabHref_old(url, localfile):
    # url local
    '''
    url = "F:\\MyProjects\\GitHub\\githubtest_old\\grabimg\\sample_html\\taobao.htm"
    soup = BeautifulSoup(open(url))
    '''
    
    # url internet
    html = urllib2.urlopen(url).read()
    html = unicode(html,'gb2312','ignore').encode('utf-8','ignore')
    #html_ = html.replace('-','_')
    #print html_
    soup = BeautifulSoup(html)
    #print soup
    content_li = soup.find('a')
    print content_li
    
    if not content_li:
        print 'it is empty here! fuck..............'
    else:
        myfile = open(localfile, 'w')
        # list for the page
        m_taobao = models.Commidity()
        list = []
        # get info 
        for item_li in content_li:
            # debug
            print item_li
            #tag_li = item_li.li
            tag_img = item_li.img
            tag_good = item_li.findAll('li', class_ = 'attr-price')
            if tag_good:
                tag_price = tag_good.span.strong.contents
            if tag_img:
                #get the url of the img
                url_download_img = tag_img['src']
                #get url
                m_taobao.url = item_li['data-item']
                m_taobao.name = tag_img['alt']
                m_taobao.price = float(tag_price)
                # for debug
                m_taobao.categories = 0
                m_taobao.sellers = 0
                # debug
                myfile.write(m_taobao)
                #print m_taobao
                # make a list
                list.append(m_taobao)
        myfile.close()
    return True
    #return localfile
