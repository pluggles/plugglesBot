#!/usr/bin/env python
import pytz
from datetime import datetime
from datetime import timedelta
from random import randint
import json
import urllib2
def getStrip(myArg= -1):
    if myArg == -1:
        myArg = str(randomNum())
        xkcd = 'https://xkcd.com/' + myArg
    elif validInput(myArg) == True:
        myArg = str(myArg)
        xkcd = 'https://xkcd.com/' + myArg
    else:
        xkcd = "That was not a valid comic number."
        return xkcd
    altText = getAltText(myArg)
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

def main():

   #p = getStrip()
   #print p
   ##p=getStrip(44)
   #print p
   #p=getStrip(7000)
   #print p
   #p=getStrip("testing")
   #print p
   #print random_date()
   getAltText(10)
   getAltText(100)
   getAltText(1000)

if __name__ == '__main__':
    main()