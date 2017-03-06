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
    else:
        myArg = str(myArg)
        xkcd = 'https://xkcd.com/' + myArg
    return xkcd

def randomNum():
    """
    This function will return a random comic number 
    objects.
    """
    obj = json.load(urllib2.urlopen("https://xkcd.com/info.0.json"))
    latest = obj["num"]
    print latest
    return randint(1, latest)

def main():

   p = getStrip()
   print p
   p=getStrip(44)
   print p
   #print random_date()

if __name__ == '__main__':
    main()