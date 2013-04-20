#coding=utf-8

import requests
import re
import sys

def _build_json_address(url):
    args= "&_input_charset=utf-8&json=on&callback=jsonp203"
    ret = re.search("(.*)\?", url)
    base_url = ret.group(1)
    ret = re.search("(spm=[^&]+)", url)
    spm = ret.group(1)
    return base_url+"?"+spm+args

def _clean_json(json_str):
    r = re.compile("\s*jsonp203\s*\(\s*([\S\s\n\r]+)\s*\)\s*", re.M)
    ret = r.search(json_str)
    return ret.group(1).encode("utf-8")

def get_json(url):
    try:
        json_url = _build_json_address(url)
        json_str = requests.get(json_url).content
        json_str = unicode(json_str, "gbk")
        return _clean_json(json_str)
    except Exception,e:
        print >> sys.stderr, "In taobao_lib.get_json:",e
    return None

if __name__ == "__main__":
    print get_json("http://list.taobao.com/itemlist/nvbao2011a.htm?spm=a2106.m894.292271.50.5MF4zK&ratesum=6%2C7%2C8%2C9%2C10%2C11%2C12%2C13%2C14%2C15%2C16%2C17%2C18%2C19%2C20&cat=50072766&isprepay=1&random=false&viewIndex=1&yp4p_page=0&commend=all&atype=b&style=grid&olu=yes&isnew=2&mSelect=false&fl=qianbaox#!cat=50072766&isprepay=1&random=false&viewIndex=1&as=0&yp4p_page=0&commend=all&atype=b&fl=qianbaox&style=grid&same_info=1&tid=0&olu=yes&isnew=2&mSelect=false&json=on&tid=0")

