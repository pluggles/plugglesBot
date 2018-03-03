#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
with open('tokenfile.txt', 'r') as tokenfile:
    myToken = tokenfile.readline().rstrip()

import telegram, random, logging, time, calendar, parsedatetime as pdt, pytz, re
import alerts, dilbert, xkcd, eightBall, fileIO, sys, fortune, helpmessages, bashQuotes, alive
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job
from datetime import datetime
from time import mktime
from pytz import timezone
from fileIO import AlertJob


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
timers = dict()
messages = dict()
users = dict()


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi! Welcome to my bot try /help')


def help(bot, update, args):

    if len(args)> 0 and args[0] == "alert":
        bot.sendMessage(update.message.chat_id,helpmessages.alertHelp())
        return
    elif len(args)> 0 and args[0] == "fortune":
        bot.sendMessage(update.message.chat_id,fortune.fortuneHelp())
        return
    elif len(args)> 0 and args[0] == "quote":
        bot.sendMessage(update.message.chat_id,helpmessages.quoteHelp())
        return
    elif len(args)> 0 and args[0] == "bash":
        bot.sendMessage(update.message.chat_id,helpmessages.bashHelp())
        return
    update.message.reply_text(helpmessages.mainHelp())

def madcow(bot, update):
    frt = fortune.fortune("off")
    message = fortune.madcow([frt])
    message = message.replace("<", "&lt;")
    message = message.replace(">", "&gt;")
    bot.sendMessage(update.message.chat_id, text="<code>"+message+"</code>", parse_mode=telegram.ParseMode.HTML)
def getcowsay(bot, update, args):
    args = ' '.join(args)
    if len(args) == 0:
        frt = fortune.fortune(args)
    else:
        frt = args
    message = fortune.cowsay([frt])
    message = message.replace("<", "&lt;")
    message = message.replace(">", "&gt;")
    bot.sendMessage(update.message.chat_id, text="<code>"+message+"</code>", parse_mode=telegram.ParseMode.HTML)
def getfortune(bot, update, args):
    args = ' '.join(args)
    bot.sendMessage(update.message.chat_id,fortune.fortune(args))
def getEightBall(bot, update, args):
    args = ' '.join(args)
    bot.sendMessage(update.message.chat_id, eightBall.isQuestion(args))
def pong(bot, update):
    update.message.reply_text("pong")
def echo(bot, update):
    update.message.reply_text(update.message.text)

def alarm(bot, job):
    """Function to send the alarm message"""
    ids = job.context.split(':')
    context = ids[0]
    
    message = messages[job.context]
    if len(message) <=0:
        message = "Alert set for right now"
    bot.sendMessage(job.context, text = message)


def alert(bot, update, args, job_queue):
    """Adds a job to the queue"""
    continueOn = 1
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    user = str(update.message.from_user)
    if (len(args) == 0):
        update.message.reply_text('please enter a time')
        return
    if '|' in args:
        message = ' '.join(args)
        argstemp = message.split('|')
        due = alerts.lastDitchAttempt(argstemp[0])
        if due > 0:
            argstemp.pop(0)
            message = ' '.join(argstemp)
            continueOn = -1
    if continueOn == 1:
        due = alerts.parseADate(args[0])
        if (due <= 0):
            due = alerts.regexmatch(args[0])
        args.pop(0)
        message = ' '.join(args)
        if due <= 0:
            update.message.reply_text('Sorry that is not a valid time')
            return 

    # Add job to queue
    myContext = '' + str(chat_id) +':' +str(message_id)
    job = Job(alarm, due, repeat=False, context=myContext)
    users[myContext] = user
    messages[myContext] = message
    timers[myContext] = job
    job_queue.put(job)
    t = datetime.now()
    due = int((t-datetime(1970,1,1)).total_seconds() + due)
    fileIO.writeAlertJob("alerts", str(chat_id), str(message_id), user, due, message)
    setFor = alerts.timeSetFor(due)
    bot.sendMessage(update.message.chat_id,'Timer successfully set for: ' + str(setFor) + '\nYour ID is:' + str(message_id))

def getDilbert(bot, update, args):
    dilbertStrip = dilbert.getStrip()
    bot.sendMessage(update.message.chat_id, dilbertStrip)
def getXkcd(bot, update, args):
    if len(args) == 0:
        xkcdUrl = xkcd.getStrip()
    else:
        xkcdNumber = ' '.join(args)
        xkcdUrl = xkcd.getStrip(xkcdNumber)
    bot.sendMessage(update.message.chat_id, xkcdUrl)
def setQuote(bot, update, args):
    chatFile = str(update.message.chat_id)
    user = str(update.message.from_user)
    message = ' '.join(args)
    response = fileIO.WriteAQuote(chatFile, message, user)
    bot.sendMessage(update.message.chat_id, response)

def removeQuote(bot, update, args):
    chatFile = str(update.message.chat_id)
    user = str(update.message.from_user)
    quoteId = args[0]
    response = fileIO.removeQuote(chatFile, quoteId, user)
    update.message.reply_text(response)

def getQuote(bot, update, args):
    chatFile = str(update.message.chat_id)
    if len(args) == 0:
        response = fileIO.getRandQuote(chatFile)
    else:
        quoteId = args[0]
        response = fileIO.getQuote(chatFile, quoteId)
    update.message.reply_text(response)
def remove(bot, update, args):
    """Removes the job if the user changed their mind"""
    try:
        myContext_id = ''.join(args)
        myContext = str(update.message.chat_id) + ':'+ myContext_id
        user = str(update.message.from_user)
        if myContext not in timers:
            update.message.reply_text('You have no active timer with code:' + myContext_id)
            return
        if user != users[myContext]:
            update.message.reply_text("You did not enter that alert!")
            return
        job = timers[myContext]
        job.schedule_removal()
        del timers[myContext]
        del messages[myContext]
        del users[myContext]
        bot.sendMessage(update.message.chat_id,'Timer successfully removed! Removed message id: ' + myContext_id)

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /alert <seconds>')

def error(bot, update, error):
    print (logger.warn('Update %s caused error %s' % (update, error)))


def findExistingAlerts(job_queue):
    try:
        myJobs = fileIO.readJobs("alerts")
        t = datetime.now()
        if myJobs != 0:
            for job in myJobs:
                due = int(job.due) - int((t-datetime(1970,1,1)).total_seconds())
                if due > 0:
                    myContext = '' + str(job.chatId) +':' +str(job.messageId)
                    myJob = Job(alarm, due, repeat=False, context=myContext)
                    users[myContext] = job.user
                    messages[myContext] = job.message
                    timers[myContext] = myJob
                    job_queue.put(myJob)
                    fileIO.writeAlertJob("alerts", job.chatId, job.messageId, job.user, job.due, job.message)
    except:
        print ("Unexpected error:", sys.exc_info())

def choice(bot, update, args):
    args = " ".join(args)
    options = args.split("|")
    sec = []
    if len(options) < 2:
        tails = "tails"
        heads = "heads"
        sec.append(tails)
        sec.append(heads)
    else:
        sec = options
    bot.sendMessage(update.message.chat_id, random.choice(sec))
    #update.message.reply_text(random.choice(sec))
def parseMessage(bot, update):
    strings = update.message.text.split( )
    subredditMatch = re.compile('^(/r/)')
    redditBase = "https://www.reddit.com"
    for word in strings:
        if re.match(subredditMatch, word):
            subreddit = redditBase + word
            if len(word) > 3:
                bot.sendMessage(update.message.chat_id, subreddit)
            #update.message.reply_text(subreddit)
def getBashQuotes(bot, update, args):
    if len(args) == 0:
        bashQuote = bashQuotes.getPost()
    else:
        specificQuoteNum = ' '.join(args)
        bashQuote = bashQuotes.getPost(specificQuoteNum)
    bot.sendMessage(update.message.chat_id, bashQuote)
def notifyxkcd(bot, update, args):
    if len(args) == 0:
        myMessage = xkcd.AddChatId(update.message.chat_id)
    elif args[0] == "remove":
        myMessage = xkcd.RemoveChatId(update.message.chat_id)
    else:
        myMessage = "That was not a valid command"
    bot.sendMessage(update.message.chat_id, myMessage)
def checkLatestxkcd(bot, job):
    newComic = xkcd.sendLatest()
    if newComic == '':
        return
    else:
        chatIds = xkcd.GetChatIds()
        for chatId in chatIds:
            bot.sendMessage(chatId, newComic)

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(myToken)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help, pass_args=True))
    dp.add_handler(CommandHandler("fortune", getfortune, pass_args=True))
    dp.add_handler(CommandHandler("cowsay", getcowsay, pass_args=True))
    dp.add_handler(CommandHandler("ping", pong))
    dp.add_handler(CommandHandler("madcow", madcow))
    dp.add_handler(CommandHandler("alert", alert, pass_args=True, pass_job_queue=True))
    dp.add_handler(CommandHandler("remove", remove, pass_args=True))
    dp.add_handler(CommandHandler("choose", choice, pass_args=True))
    # Quote functions
    dp.add_handler(CommandHandler("setquote", setQuote, pass_args=True))
    dp.add_handler(CommandHandler("removequote", removeQuote, pass_args=True))
    dp.add_handler(CommandHandler("quote", getQuote, pass_args=True))
    dp.add_handler(CommandHandler("dilbert", getDilbert, pass_args=True))
    dp.add_handler(CommandHandler("xkcd", getXkcd, pass_args=True))
    dp.add_handler(CommandHandler("notifyxkcd", notifyxkcd, pass_args=True))
    dp.add_handler(CommandHandler("bash", getBashQuotes, pass_args=True))
    dp.add_handler(CommandHandler("8ball", getEightBall, pass_args=True))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler([Filters.text], parseMessage))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    findExistingAlerts(updater.job_queue)
    xkcd.ReadLatestFromFile()
    xkcd.getLatests()
    myJob = Job(checkLatestxkcd, 900, repeat=True, context="myContext")
    updater.job_queue.put(myJob)
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
