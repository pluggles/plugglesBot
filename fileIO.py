#!/usr/bin/env python
### Helper class to read and write to files
import cPickle as pickle
import os
import bisect
import sys
import random
class AlertJob(object):
	def __init__(self,chatId, messageId, user, due, message):
		self.chatId = chatId
		self.messageId = messageId
		self.user = user
		self.due = due
		self.message = message

class Quote(object):
	def __init__(self, quoteId, message, user):
		self.quoteId = quoteId
		self.message = message
		self.user = user

def writeAlertJob(WriteTo, chatID, messageid, user, due, message):
	myJob = AlertJob(chatID, messageid, user, due, message)
	with open(WriteTo, "ab") as myfile:
		pickle.dump(myJob, myfile, -1)
	del myJob

def readJobs(readFrom):
	myJobs = []
	try:
		f = open(readFrom, 'r+b')
		while True:
			try:
				myJobs.append(pickle.load(f))
			except EOFError:
				os.remove(readFrom)
				break
		return myJobs
	except IOError:
		print (f"File: {readFrom} can not be opened for reading.")
	return 0

def getQuote(readFrom, quoteID):
	quotes = []
	readFrom = readFrom + "/" + readFrom
	try:
		f = open(readFrom, 'r+b')
		while True:
			try:
				quotes.append(pickle.load(f))
			except EOFError:
				f.close()
				break
		for quote in quotes:
			if str(quote.quoteId) == str(quoteID):
				return quote.message
		return "No quote with that ID found."
	except (OSError, IOError):
		return "No quotes made in this chat."
	except:
		return "No quote found or there was an error"

def getRandQuote(readFrom):
	quotes = []
	readFrom = readFrom + "/" + readFrom
	if not os.path.exists(os.path.dirname(readFrom)):
	    try:
	        os.makedirs(os.path.dirname(readFrom))
	    except OSError as exc: # Guard against race condition
	        if exc.errno != errno.EEXIST:
	            raise
	try:
		f = open(readFrom, 'r+b')
		while True:
			try:
				quotes.append(pickle.load(f))
			except EOFError:
				f.close()
				break
		if len(quotes) != 0:
			quote = random.choice(quotes)
			prefix = "Quote: " + str(quote.quoteId) + "\n"
			return prefix + quote.message 
		else:
			return "No quotes made in this chat"
	except (OSError, IOError):
		return "No quotes made in this chat."
	except:
		print "error happned in getRandQuote ", sys.exc_info()[0] 
		return "No quote found or there was an error"
def removeQuote(readFrom, quoteID, user):
	quotes = []
	qutefound = 0
	readFrom = readFrom + "/" + readFrom
	try:
		f = open(readFrom, 'r+b')
		while True:
			try:
				quotes.append(pickle.load(f))
			except EOFError:
				f.close()
				break
		for quote in quotes:
			if str(quote.quoteId) == str(quoteID) and str(quote.user) == str(user):

				quotes.remove(quote)
				os.remove(readFrom)
				quotefound = 1
				break
			if quote.quoteId == quoteID:
				return "You didn't make that quote!"
		if quotefound != 1:
			return "No quote with that id found."
	except (OSError, IOError):
		return "No quotes made in this chat."
	except:
		return "No quote found"
	try:
		with open(readFrom, "ab") as myfile:
			for quote in quotes:
				pickle.dump(quote, myfile, -1)
		freeUpKey(readFrom, quoteID)
		return "Quote removed"
	except (OSError, IOError):
		return "Something bad happend related to fileIO, all your quotes are gone, I should probably start using a database."
	except:
		return "Something bad happend, all your quotes are gone, I should probably start using a database."

def freeUpKey(readfrom, quoteId):
	try:
		myfile = str(readfrom) + "quoteIds"
		f = open(myfile, "r+b")
		d = f.read().splitlines() 
		f.seek(0)
		for i in d:
			if str(i) != str(quoteId):
				f.write("%s\n" % i)
		f.truncate()
		f.close()
	except:
		print "error happned in free up key ", sys.exc_info()[0]

def getQuoteId(writeTo):
	if not os.path.exists(os.path.dirname(writeTo)):
	    try:
	        os.makedirs(os.path.dirname(writeTo))
	    except OSError as exc: # Guard against race condition
	        if exc.errno != errno.EEXIST:
	            raise
	myfile = str(writeTo) + "quoteIds"
	ids = []
	newid = 1
	try:
		with open(myfile, "rb") as myFile:
			ids = [line.rstrip('\n') for line in myFile]
		ids = map(int, ids)
		ids = sorted(ids)
		os.remove(myfile)
	except:
		print "error opening and getting ids"
	try:
		uniqueId = 0
		if len(ids) == 0:
			ids.append(uniqueId)
			with open(myfile, "w+b") as myFile:
				for item in ids:
					myFile.write("%s\n" % item)
			return uniqueId
		
		while uniqueId < len(ids):
			if uniqueId in ids:
				uniqueId = uniqueId+1
			else:
				ids.append(uniqueId)
				break
		ids.append(uniqueId)
		with open(myfile, "w+b") as myFile:
			for item in ids:
				myFile.write("%s\n" % item)
		return str(uniqueId)
	except:
		print "Error found getting id " + str(sys.exc_info())
def WriteAQuote(WriteTo, quote, user):
	WriteTo = WriteTo + "/" + WriteTo
	if not os.path.exists(os.path.dirname(WriteTo)):
	    try:
	        os.makedirs(os.path.dirname(WriteTo))
	    except OSError as exc: # Guard against race condition
	        if exc.errno != errno.EEXIST:
	            raise
	quoteID = getQuoteId(WriteTo)
	myQuote = Quote(quoteID, quote, user)
	with open(WriteTo, "ab") as myfile:
		pickle.dump(myQuote, myfile, -1)
	del myQuote
	return "Quote %s Added." %(quoteID)

def main():
	print "hello"
	WriteAQuote("0123", "quote", "123")
	WriteAQuote("0123", "quote 2", "123")
	getQuote("0123", "1")
	getRandQuote("0123")
	removeQuote("0123", "1", "123")
	getRandQuote("0123")

if __name__ == '__main__':
	main()