#!/usr/bin/env python
import time, calendar, parsedatetime as pdt, pytz, re
from datetime import datetime
from time import mktime
from pytz import timezone
from dateutil import tz

c = pdt.Constants()
c.BirthdayEpoch = 80
p = pdt.Calendar(c)
dateFormats = ["%d/%m/%y-%H:%M:%S", "%d/%m/%y", "%d/%m/%Y", "%d/%m/%y-%H:%M", "%d/%m/%Y-%H:%M:%S", "%d/%m/%y-%H:%M", "%H:%M:%S"]
#will try to match a time given in a form of hh:mm:ss from current time
def regexmatch(timestring):

	pattern = re.compile("^(?:(?:([0-9])*:)?([0-9]*?\d):)?([0-9]*\d)$")
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
	time = 3600*hours + 60*mins + secs
	return time
#will try and find the time from any date formate
def lastDitchAttempt(myTime):
	currentTime = datetime.now()
	try:
		time_struct, parse_status = p.parse(myTime)
		d = datetime.fromtimestamp(mktime(time_struct))
		returntime = d - currentTime
		return int(returntime.total_seconds())
	except ValueError:
		pass
	return -1
# will try to get the time from my list of known date formats
def parseADate(myTime):
	currentTime = datetime.now()
	for fmt in dateFormats:
		try:
			d = datetime.strptime(myTime, fmt)
			returntime = d - currentTime
			return int(returntime.total_seconds())
		except ValueError:
			pass
	return -1
def timeSetFor(due):
	#t = datetime.now()
	#due = int((t-datetime(1970,1,1)).total_seconds() + due)
	from_zone = tz.tzutc()
	to_zone = tz.tzlocal()
	utc =  datetime.fromtimestamp(due)
	utc = utc.replace(tzinfo=to_zone)
	local = utc.astimezone(from_zone)
	return local.strftime('%d/%m/%y-%H:%M:%S EST')
def main():
	t = timeSetFor(10)

if __name__ == '__main__':
	main()