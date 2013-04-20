# -*- coding:utf8 -*-
'''
Created on Jan 16, 2013

@author: surecc
'''
'''
import urllib2
import chardet
import sys

req = urllib2.Request("http://www.taobao.com/")
res = urllib2.urlopen(req)
html = res.read()
web_encode = chardet.detect(html)['encoding']
local_encode = sys.getdefaultencoding()
res.close()

html = html.decode(web_encode).encode(local_encode)
print html

'''