#!/usr/bin/env python
import pytz, sys, requests
from datetime import datetime
from datetime import timedelta
from random import randint
import json
import urllib2, urllib
import re

LatestComic = 0
Updated = False
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
    elif myArg == '0':
        myArg = str(getLatests())
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
def sendLatest():
    latest = getLatests()
    if Updated == True:
        xkcd = 'https://xkcd.com/' + str(latest)
        altText = getAltText(latest)
        return xkcd + "\n" + altText
    return ''

def getLatests():
    global Updated
    try:
        obj = json.load(urllib2.urlopen("https://xkcd.com/info.0.json"))
        latest = int(obj["num"])
        Updated = storeLatest(latest)
        return latest
    except:
        print "returning 1"
        return 1
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
        #print query
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
def storeLatest(latest):
    try:
        global LatestComic
        if int(LatestComic) != int(latest):
            LatestComic = int(latest)
            WriteLatest()
            return True
        return False
    except:
        print "error", sys.exc_info()[0]
        return False
def WriteLatest():
    global LatestComic
    f = open('latestxkcd.txt', 'w')
    f.write(str(LatestComic))
    f.close()
def ReadLatestFromFile():
    global LatestComic
    f = open('latestxkcd.txt', 'r')
    LatestComic= f.read().strip()
    print "Read in: " + str(LatestComic)
    f.close()
def AddChatId(myId):
    try:
        file = 'xkcdChannels.txt'
        with open(file) as f:
            lines = f.read().splitlines()
        if str(myId) in lines:
            return "This chat is already receiving new xkcd notifcations"
        else:
            lines.append(str(myId))
            f = open(file, 'w')
            for line in lines:
                f.write("%s\n" % line)
            f.close
            return "Chat will now get notified of new xkcds"
    except:
        print "error", sys.exc_info()[0]
        return "something terrible may have just happened"
def RemoveChatId(myId):
    try:
        file = 'xkcdChannels.txt'
        with open(file) as f:
            lines = f.read().splitlines()
        if str(myId) in lines:
            lines.remove(str(myId))
            f = open(file, 'w')
            for line in lines:
                f.write("%s\n" % line)
            f.close
            return "Chat will no longer be notified of new xkcds"
        else:
            return "This chat isn't currently getting notified of new xkcds"
            
    except:
        print "error", sys.exc_info()[0]
        return "something terrible may have just happened"
def GetChatIds():
    file = 'xkcdChannels.txt'
    with open(file) as f:
        lines = f.read().splitlines()
    return lines

def main():

   #p = getStrip()
   #print p
   #p=getStrip(44)
   #print p
   #p=getStrip(7000)
   #print p
   #p=getStrip("testing")
   #print p
   #p=getStrip("linux")
   #print p
   #p=getStrip("444")
   #print p
   #p=getStrip('0')
   #print p
   #ReadLatestFromFile()
   #p = sendLatest()
   #print p
   p = AddChatId(10)
   print p
   p = AddChatId(20)
   print p
   p = AddChatId(15)
   print p
   p = AddChatId(100)
   print p
   p = GetChatIds()
   for word in p:
    print word
   p = RemoveChatId(5)
   print p
   p = RemoveChatId(10)
   print p
   p = GetChatIds()
   for word in p:
    print word



   

if __name__ == '__main__':
    main()
