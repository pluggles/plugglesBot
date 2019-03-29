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
import os
import re
import sys

def AddChatId(myId):
    try:
        file = 'motorcycle.txt'
        EnsureFileExists(file)
        with open(file) as f:
            lines = f.read().splitlines()
        if str(myId) in lines:
            return "This chat is already receiving new motorcycle notifcations"
        else:
            lines.append(str(myId))
            f = open(file, 'w')
            for line in lines:
                f.write("%s\n" % line)
            f.close
            return "Chat will now get notified of new motorcycle updates"
    except:
        print "error", sys.exc_info()[0]
        return "something terrible may have just happened"
def RemoveChatId(myId):
    try:
        file = 'motorcycle.txt'
        EnsureFileExists(file)
        with open(file) as f:
            lines = f.read().splitlines()
        if str(myId) in lines:
            lines.remove(str(myId))
            f = open(file, 'w')
            for line in lines:
                f.write("%s\n" % line)
            f.close
            return "Chat will no longer be notified of new motorcycle updates"
        else:
            return "This chat isn't currently getting notified of new motorcycle"
            
    except:
        print "error", sys.exc_info()[0]
        return "something terrible may have just happened"
def GetChatIds():
    file = 'motorcycle.txt'
    EnsureFileExists(file)
    with open(file) as f:
        lines = f.read().splitlines()
    return lines
def EnsureFileExists(filename):
    if not os.path.exists(filename):
        file(filename, 'w').close()

def getCount():
    """Summary

    Returns:
        TYPE: Description
    """

    url = 'https://axiom.lcc.edu/wconnect/ace1/ShowSchedule.awp1?&Criteria=UPPER%28cocrsenm%29%20LIKE%20%27BASIC%20RIDER%20COURSE%25%27&TITLE=Title%20begins%20with%20%22basic%20rider%20course%22'
    #content = urllib2.urlopen(url).readlines()
    #print content
    r = urllib.urlopen(url).read()
    #print r
    soup = BeautifulSoup(r, "lxml")
    table = soup.findChildren("table", {"class" : "awTable"})
    table = table[0]
    rows = table.findChildren("tr")
    #print rows
    return len(rows)


def main():
    """Summary
    """
    print getCount()


if __name__ == '__main__':
    main()
