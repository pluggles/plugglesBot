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
import json
import yaml

def AddChatId(myId):
    try:
        file = 'masa.txt'
        EnsureFileExists(file)
        with open(file) as f:
            lines = f.read().splitlines()
        if str(myId) in lines:
            return "This chat is already receiving new masa notifcations"
        else:
            lines.append(str(myId))
            f = open(file, 'w')
            for line in lines:
                f.write("%s\n" % line)
            f.close
            return "Chat will now get notified of new masa updates"
    except:
        print "error", sys.exc_info()[0]
        return "something terrible may have just happened"
def RemoveChatId(myId):
    try:
        file = 'masa.txt'
        EnsureFileExists(file)
        with open(file) as f:
            lines = f.read().splitlines()
        if str(myId) in lines:
            lines.remove(str(myId))
            f = open(file, 'w')
            for line in lines:
                f.write("%s\n" % line)
            f.close
            return "Chat will no longer be notified of new masa updates"
        else:
            return "This chat isn't currently getting notified of new masa updates"
            
    except:
        print "error", sys.exc_info()[0]
        return "something terrible may have just happened"
def GetChatIds():
    file = 'masa.txt'
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

    url = 'https://mistaff.com/wp-json/frm/v2/views/375?exclude_script=formidable,jquery-core,jquery-migrate,jquery,slicknavjs,slicknav-init,slicknavjs,slicknav-init,mistaff-navigation,mistaff-skip-link-focus-fix&county=&position=Teacher&jobtype=full+time&text='
    #content = urllib2.urlopen(url).readlines()
    #print content
    r = urllib.urlopen(url).read()
    as_json = json.loads(r)
    #print r
    soup = BeautifulSoup(as_json.get("renderedHtml"), "lxml")
    # print soup
    table = soup.findChildren(id="job-results")
    # print table
    table = table[0]
    rows = table.findChildren("tr")
    active_jobs = parse_rows(rows)
    previous_jobs = get_previous_jobs()
    new_jobs = find_diff(active_jobs, previous_jobs)
    write_jobs(active_jobs)
    message = format_message(new_jobs, active_jobs)

    
        
    return message

def format_message(new_jobs, active_jobs):
    message = "Found the following new listings:\r\n"
    for id in new_jobs:
        message = message + "\r\n"
        job = active_jobs.get(id)
        print "job", job
        message = message + "[%s](%s)\r\n" % (job.get("name"), job.get("url"))
        message = message + "district: %s\r\n" %(job.get("District/Organization"))
        message = message + "county: %s\r\n" %(job.get("County"))
        print message
    return message

def find_diff(active_jobs, saved_jobs):
    if not saved_jobs:
        return active_jobs.keys()
    new_jobs = set(active_jobs) - set(saved_jobs)
    # print "new jobs ", new_jobs
    # for id in new_jobs:
    #     print active_jobs.get(id)
    return new_jobs


def get_previous_jobs():
    file = 'jobs.txt'
    EnsureFileExists(file)
    with open(file, 'r') as f:
        jobs = yaml.safe_load(f)
    # print jobs
    return jobs

def write_jobs(jobs):
    try:
        file = 'jobs.txt'
        EnsureFileExists(file)
        f = open(file, 'w')
        f.write(json.dumps(jobs))
        f.close
    except:
        print "error", sys.exc_info()[0]
        return "something terrible may have just happened"

def parse_rows(rows):
    relevant_rows = {}
    for row in rows[1:]:
        job = {}
        for data in row.findChildren("td"):
            # print "data: ", data
            # print data
            if data.a:
                # print data.a
                # print data.a.attrs['href']
                # print data.a.text
                key = str(data.a.attrs['href'].partition("=")[2])
                job["url"] = str(data.a.attrs['href'])
                job["name"] = data.a.text.encode('utf-8', 'ignore')
            for span in data.find_all('span'):
                # print data.__dict__
                job[str(span.text)[:-2]] = data.text.replace(span.text.encode('utf-8'), "").encode('utf-8')
        # print "job: ", job
        relevant_rows[key] = job
    # print relevant_rows
    return relevant_rows
    


def main():
    """Summary
    """
    print getCount()


if __name__ == '__main__':
    main()
