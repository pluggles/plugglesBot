#!/usr/bin/env python
import pytz
from datetime import datetime
from datetime import timedelta
from random import randrange
def getStrip():
    randDate = random_date()
    comicDate = randDate.strftime("%Y-%m-%d")
    url = 'http://dilbert.com/strip/' + comicDate
    return url

def random_date():
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    start = datetime.strptime('1989-04-16', '%Y-%m-%d')
    end = datetime.now()
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

def main():

   p = getStrip()
   print p

if __name__ == '__main__':
    main()