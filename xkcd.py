#!/usr/bin/env python
import pytz
from datetime import datetime
from datetime import timedelta
from random import randrange
def getStrip(myArg= -1):
    if myArg == -1:
        xkcd = 'c.xkcd.com/random/comic/'
    else:
        myArg = str(myArg)
        xkcd = 'https://xkcd.com/' + myArg
    return xkcd

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
   p=getStrip(44)
   print p

if __name__ == '__main__':
    main()