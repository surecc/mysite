'''
Created on Jan 16, 2013

@author: surecc
'''
#grab the href
from bs4 import BeautifulSoup 
import urllib2
import re
#grab the urls of website and save into localfile
def grabHref(url, localfile):
    html = urllib2.urlopen(url).read()
    html = unicode(html,'gb2312','ignore').encode('utf-8','ignore')
    content = BeautifulSoup(html).findAll('a')
    myfile = open(localfile,'w')
    pat1 = re.compile(r'href="([^"]*)"')
    pat2 = re.compile(r'http')
    ans = ""
    for item in content:
        # debug
        #print item
        h_tmp = pat1.search(str(item))
        if h_tmp:
            href = h_tmp.group(1)
            if pat2.search(href):
                ans = href
            else:
                ans = url+href
        myfile.write(ans)
        myfile.write('\r')
        #debug
        #print ans
    myfile.close()
    return ans 
    #return localfile