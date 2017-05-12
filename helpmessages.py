#!/usr/bin/env python
def mainHelp():
	return """I can do a few things.
Try '/help alert' or '/help fortune or /help quote or even /help bash'

That is basically it, and I am probably prone to breaking, and a shit ton of errors
If I break I break deal with it.
I plan on adding stuff at some point maybe."""

def alertHelp():
	return """To set a message use: 
    '/alert <time> your message'
Time can be:
	d/m/y-H:M:S
	d/m/Y-H:M:S
	d/m/y
	d/m/Yd
	d/m/y-H:M
	d/m/y-H:M
	H:M:S
	M:S
Want to try a date format not listed?
Just split the time and your message with a pipe "|":
	/alert in 2 weeks at noon | do stuff
	/alert nov 25 | do stuff
	/alert 9:55pm | do stuff
	etc etc
And see if it works (it probbably will not)
To remove you message use: 
    '/remove <messageID>'"""

def quoteHelp():
	return """Set, get or remove a quote.
	usage:
	/quote <id>  :  gets a made quote from the chat you are in.
	/setquote <message>  : sets a quote
	/removequote <id>  :  removes a quote"""

def bashHelp():
	return """ Reutrns a quote from bash.org.
	usage:
	/bash : gets a random quote
	/bash <id> : gets a specific quote
	/bash top : get one of the top 200 quotes at random
	"""