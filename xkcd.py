#!/usr/bin/env python
import pytz, sys, requests
from datetime import datetime
from datetime import timedelta
from random import randint
import json
import urllib2, urllib
import re
def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
def getStrip(myArg= -1):
    if myArg == -1:
        myArg = str(randomNum())
        xkcd = 'https://xkcd.com/' + myArg
        altText = getAltText(myArg)
    elif RepresentsInt(myArg) == False:
        myArg = getKeyWord(myArg)
        if myArg != -1:
            xkcd = 'https://xkcd.com/' + myArg
            altText = getAltText(myArg)
        else:
            xkcd = "Something bad happened"
            return xkcd
    elif validInput(myArg) == True:
        myArg = str(myArg)
        xkcd = 'https://xkcd.com/' + myArg
        altText = getAltText(myArg)
    else:
        xkcd = "That was not a valid comic number."
        return xkcd
    return xkcd + "\n" + altText 
def validInput(arg):
    try:
        obj = json.load(urllib2.urlopen("https://xkcd.com/info.0.json"))
        latest = int(obj["num"])
        if int(arg) in range(1, latest):
            return True
        return False
    except ValueError:
        return False
def getAltText(id):
    try:
        url = "https://xkcd.com/" + str(id) + "/info.0.json"
        obj = json.load(urllib2.urlopen(url))
        altText = obj["alt"]
        return altText
    except:
        return
def randomNum():
    """
    This function will return a random comic number 
    objects.
    """
    obj = json.load(urllib2.urlopen("https://xkcd.com/info.0.json"))
    latest = obj["num"]
    return randint(1, latest)
def getKeyWord(keywords):
    try:
        query = keywords
        query = urllib.quote_plus(query)
        print query
        url = 'https://relevantxkcd.appspot.com/process?action=xkcd&query=' + query
        content = urllib2.urlopen(url).readlines()
        line = content[2].split(' ', 1)
        id = line[0]
        return id
    except:
        print "error", sys.exc_info()[0]
        return -1
def ungzipResponse(r,b):
    headers = r.info()
    if headers['Content-Encoding']=='gzip':
        import gzip
        gz = gzip.GzipFile(fileobj=r, mode='rb')
        html = gz.read()
        gz.close()
        headers["Content-type"] = "text/html; charset=utf-8"
        r.set_data( html )
        b.set_response(r)

def main():

   p = getStrip()
   #print p
   p=getStrip(44)
   #print p
   p=getStrip(7000)
   #print p
   p=getStrip("testing")
   print p
   p=getStrip("linux")
   print p
   p=getStrip("444")
   #print p
   

if __name__ == '__main__':
    main()
