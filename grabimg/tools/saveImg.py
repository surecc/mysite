import requests
import re
import os
import sys
def saveImgTux():
    res = requests.get(sys.argv[1])
    urls = re.findall('(//[^"]+/\w+/src/([0-9]+.\w+))', res.content)
    
    pics = {}
    for url, file_name in urls:
        pics["http:" + url] = file_name
    
    try : os.mkdir("./4chan/")
    except: pass
    
    PATH = lambda x : "./4chan/%s" % (x)
    
    for u, f in pics.items():
        if os.path.exists(PATH(f)):
            continue
        res = requests.get(u)
        if res.status_code == 200:
            print "Saved", PATH(f)
            pic_file = open(PATH(f), "wb")
            print >> pic_file, res.content
            pic_file.close()
        


import urllib   
def saveImg(url, path):
    #url = r"http://www.iteye.com/images/logo.gif"  
    #path = r"h:\downloads\1.jpg"  
    data = urllib.urlopen(url).read()   
    f = file(path,"wb")   
    f.write(data) 
    f.close() 
