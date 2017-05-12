#!/usr/bin/env python
import pytz
from datetime import datetime
from datetime import timedelta
import random
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
    elif (postNumber == 'top'):
        return randTop()
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

def randTop():
    if random.random() < .5:
        page = 1
    else:
        page = 2
    url = 'http://bash.org/?top' + str(page)
    content = urllib2.urlopen(url).readlines()
    #print content
    r = urllib.urlopen(url).read()
    #print r
    soup = BeautifulSoup(r, "lxml")
    mydivs = soup.findAll("p", { "class" : "qt" })
    randTop = random.randint(0, 99)
    return mydivs[randTop].text.encode('utf-8')
    
def RepresentsInt(s):

    try: 
        int(s)
        return True
    except ValueError:
        return False

def main():
    print getPost('top')


if __name__ == '__main__':
    main()