#!/usr/bin/env python
"""Summary
"""
import pytz
from datetime import datetime
from datetime import timedelta
import random
import lxml
from bs4 import BeautifulSoup
import urllib
import urllib2, urllib
import collections
import re

def get_post(post_number=-1):
    """Summary
    Args:
        post_number (TYPE, optional): Description
    Returns:
        TYPE: Description
    """
    if post_number == -1:
        return random_quote()
    elif post_number == 'top':
        return rand_top()
    elif not represents_int(post_number):
        return getKewordPost(post_number)
    elif represents_int(post_number):
        return getSpecificPost(post_number)

def getKewordPost(keywords):
    """Summary
    Args:
        keywords (TYPE): Description
    Returns:
        TYPE: Description
    """
    query = keywords
    query = urllib.quote_plus(query)
    url = 'http://bash.org/?search=' +query +'&sort=0&show=25'
    #content = urllib2.urlopen(url).readlines()
    #print content
    r = urllib.urlopen(url).read()
    #print r
    soup = BeautifulSoup(r, "lxml")

    mydivs = soup.findAll("p", {"class" : "qt"})
    for row in mydivs:
        return row.text.encode('utf-8')
    return "No quote found matching that search term..."

def random_quote():
    """Summary

    Returns:
        TYPE: Description
    """
    url = 'http://www.bash.org/?random'
    #content = urllib2.urlopen(url).readlines()
    #print content
    r = urllib.urlopen(url).read()
    #print r
    soup = BeautifulSoup(r, "lxml")

    mydiv = soup.find("p", {"class" : "qt"})
    return mydiv.text

def getSpecificPost(post):
    """Summary

    Args:
        post (TYPE): Description

    Returns:
        TYPE: Description
    """
    url = 'http://www.bash.org/?' + str(post)
    #content = urllib2.urlopen(url).readlines()
    #print content
    r = urllib.urlopen(url).read()
    #print r
    soup = BeautifulSoup(r, "lxml")

    mydivs = soup.findAll("p", {"class" : "qt"})
    for row in mydivs:
        return row.text.encode('utf-8')
    return "That quote does not exist..."

def rand_top():
    """Summary

    Returns:
        TYPE: Description
    """
    if random.random() < .5:
        page = 1
    else:
        page = 2
    url = 'http://bash.org/?top' + str(page)
    #content = urllib2.urlopen(url).readlines()
    #print content
    r = urllib.urlopen(url).read()
    #print r
    soup = BeautifulSoup(r, "lxml")
    mydivs = soup.findAll("p", {"class" : "qt"})
    rand_top_post = random.randint(0, 99)
    return mydivs[rand_top_post].text.encode('utf-8')

def get_HTML(url):
    """Summary
    
    Args:
        url (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    #content = urllib2.urlopen(url).readlines()
    #print content
    return urllib.urlopen(url).read()
    #print r

def represents_int(value):
    """Summary

    Args:
        s (TYPE): Description

    Returns:
        TYPE: Description
    """
    try:
        int(value)
        return True
    except ValueError:
        return False

def main():
    """Summary
    """
    print getKewordPost('twitter')


if __name__ == '__main__':
    main()
