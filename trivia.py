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
import requests
import collections
import re
"""
TODO: add way to set anc change trivia state
"""
def get_hint():
    """Summary
    Args:
        Gets tge hint of the weak
    Returns:
        TYPE: Description
    """

    url = 'http://teamtriviami.com/'
    request = urllib.urlopen(url).read()
    #print r
    soup = BeautifulSoup(request, "lxml")

    mydivs = soup.find_all("span", {"class" : "hasCaption"})
    #print mydivs
    for row in mydivs:
        clue = row.text.encode('utf-8').strip()
        match = re.search("(TEAM TRIVIA HINT OF THE WEEK .* -)", clue)
        if match:
            clue = match.group(1)
            clue = clue[:-2]
            return clue
    return "Error finding clue of the week, try looking yourself at: http://teamtriviami.com"


def get_answer():
    """Summary
    Args:
        keywords (TYPE): Description
    Returns:
        TYPE: Description
    """
    stateId = 105
    """ 
    POST
    URL: https://www.teamtrivia.com/selectregion.php?m=select&p=aon
    Body: region_ID=105
    """
    url = 'https://www.teamtrivia.com/answerofthenight.php'
    #content = urllib2.urlopen(url).readlines()
    #print content
    s = requests.Session()
    s.post('https://www.teamtrivia.com/selectregion.php?m=select&p=aon', data = {'region_ID' : '105'})
    request = s.get(url)
    #print r
    soup = BeautifulSoup(request.text, "lxml")

    for divs in soup.find_all("div", {"class" : "card-body"}):
        for answer in divs.find_all("h2"):
            return (answer.text.encode('utf-8'))
    return ('Error Looking up answer go here: %s' %url)


def get_trivia():
    """Summary

    Args:
        s (TYPE): Description

    Returns:
        TYPE: Description
    """
    try:
        hint = get_hint()
        answer = get_answer()
        return ("%s \r\nANSWER OF THE DAY: %s" %(hint,answer))
    except:
        return False

def main():
    """Summary
    """
    print get_trivia()


if __name__ == '__main__':
    main()
