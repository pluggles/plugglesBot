#!/usr/bin/env python
import pytz
from datetime import datetime
from datetime import timedelta
from random import randrange
from bs4 import BeautifulSoup
import urllib
import urllib2, urllib
import collections
import re

def getPost(postNumber = -1):
    if (postNumber == -1):
        return random_quote()
    elif RepresentsInt(postNumber) == True:
       return getSpecificPost(postNumber)
    else:
        return "That was not a valid input try a number."

def random_quote():
    url = 'http://www.bash.org/?random'
    content = urllib2.urlopen(url).readlines()
    #print content
    r = urllib.urlopen(url).read()
    #print r
    soup = BeautifulSoup(r, "lxml")

    mydiv = soup.find("p", { "class" : "qt" })
    return mydiv.text

def getSpecificPost(post):
    url = 'http://www.bash.org/?' + str(post)
    content = urllib2.urlopen(url).readlines()
    #print content
    r = urllib.urlopen(url).read()
    #print r
    soup = BeautifulSoup(r, "lxml")

    mydivs = soup.findAll("p", { "class" : "qt" })
    for row in mydivs:
        return row.text.encode('utf-8')
    return "That quote does not exist..."
def RepresentsInt(s):

    try: 
        int(s)
        return True
    except ValueError:
        return False

def main():
    print getPost(2258)


if __name__ == '__main__':
    main()