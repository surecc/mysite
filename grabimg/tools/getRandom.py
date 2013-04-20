'''
Created on Jan 15, 2013

@author: surecc
'''

# get the ramdom string 

import random
import string
def getRandomStr(i):
    rd1 = random.sample('qwertyuiopasdfghjklzxcvbnm12234567890', i)
    rd2 = string.join(rd1).replace(" ","")
    return rd2

import uuid
def getUUID():
    return str(uuid.uuid4())

import md5
def getMD5(str):
    return md5.md5(str)

import hashlib
def getHash(str):
    m = hashlib.md5()
    m.update(str)
    m.digest()
    return m
