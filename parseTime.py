#!/usr/bin/env python
from datetime import datetime
import time
from time import mktime
import calendar
import parsedatetime as pdt
import pytz
from pytz import timezone
import re

c = pdt.Constants()

c.BirthdayEpoch = 80
p = pdt.Calendar(c)
dateFormats = ["%d/%m/%y-%H:%M:%S", "%d/%m/%y", "%d/%m/%Y", "%d/%m/%y-%H:%M", "%d/%m/%Y-%H:%M:%S", "%d/%m/%y-%H:%M", "%H:%M:%S"]
def getSeconds(timeString):
	print "parsing " + timeString
    	try:
    		return int(timeString)
    	except ValueError:
    		pass
    	try:
    		#print "trying complicated parsing"
    		time_struct, parse_status = p.parseDT(datetimeString =timeString, tzinfo=timezone("US/Eastern"))
    		seconds = int(time.mktime(time_struct.timetuple()) - calendar.timegm(time.gmtime()))
    		return seconds

    	except ValueError:
    		#print 
    		pass
    	return -1

def regexmatch(timestring):
	pattern = re.compile("^(?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d)$")
	print "regex trying: " + timestring
	hours = mins = secs = 0
	if pattern.match(timestring):
		args = timestring.split(":")
		if len(args) == 3:
			hours = int(args[0])
			mins = int(args[1])
			secs = int(args[2])
		elif len(args) == 2:
			mins = int(args[0])
			secs = int(args[1])
		else:
			secs = int(args[0])
	time = 1200*hours + 60*mins + secs
	return time


def parseADate(myTime):
	print "Trying to parse: " + myTime
	currentTime = datetime.now()
	#currentTime = int(time.mktime(currentTime.timetuple()))
	print "currentTime is: " + str(currentTime)
	for fmt in dateFormats:
		try:
			d = datetime.strptime(myTime, fmt)
			returntime = d - currentTime
			print d
			print returntime
			return int(returntime.total_seconds())

			return
		except ValueError:
			pass
	return -1

def lastDitchAttempt(myTime):
	print "Trying to parse: " + myTime
	currentTime = datetime.now()
	#currentTime = int(time.mktime(currentTime.timetuple()))
	print "currentTime is: " + str(currentTime)
	try:
		time_struct, parse_status = p.parse(myTime)
		d = datetime.fromtimestamp(mktime(time_struct))
		returntime = d - currentTime
		print d
		print int(returntime.total_seconds())
		return 
	except ValueError:
		pass
	print "failed"
	return
def main():
	myList = ['abc', 'ab|', 'testing', '|']
	if '|' in myList:
		print 'found'
	'''	
    # Create the EventHandler and pass it your bot's token.
    dateTime = []
    #dateTime.append('12/10/1992')
    #dateTime.append('12/10/1992-23:10:54')
    #dateTime.append('12/10/1992-22:10:54')
    #dateTime.append('1/1/01-0:0:0')
    #dateTime.append('05/05/16')
    #dateTime.append('20:10:53')
    #dateTime.append('19/10/2016')
    #dateTime.append('19/10/16-19:22:15')
   # dateTime.append('20/10/2016-20:09:00')
    dateTime.append('26/02/2017')
    dateTime.append('26/02/2017-10:00:00')
    dateTime.append('4pm tomorrow')
    dateTime.append('in 2 hours')
    dateTime.append('2h4m30s')
    #dateTime.append('19/10/16')
    dateTime.append('')
    dateTime.append('')
    dateTime.append('')
    dateTime.append('')
    dateTime.append('')
    dateTime.append('')
    dateTime.append('')
    dateTime.append('')
    '''
    #for currentdate in dateTime:
    	#parseADate(currentdate)
    	'''seconds = getSeconds(currentdate)
    	print "using get seconds: " + str(seconds)
    	seconds = regexmatch(currentdate)
    	print "using regex seconds: " + str(seconds)
		'''
    	#lastDitchAttempt(currentdate)



if __name__ == '__main__':
    main()