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

Attributes:
    logger (TYPE): Description
    messages (TYPE): Description
    timers (TYPE): Description
    users (TYPE): Description
"""
with open('tokenfile.txt', 'r') as tokenfile:
    MYTOKEN = tokenfile.readline().rstrip()


import random
import logging
#import time
#import calendar
import sys
#import parsedatetime as pdt
#import pytz
import re
from datetime import datetime
#from time import mktime
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job
#from pytz import timezone
import alerts
import dilbert
import xkcd
import eightBall
import fileIO
#from fileIO import AlertJob
import fortune
import helpmessages
import bashQuotes
import motorcycleUpdates


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

LOGGER = logging.getLogger(__name__)
TIMERS = dict()
MESSAGES = dict()
USERS = dict()


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Summary
        First response when the bot is started
    Args:
        bot (TYPE): The bot, always good to send
        update (TYPE): the message handler
    """
    update.message.reply_text('Hi! Welcome to my bot try /help')


def bot_help(bot, update, args):
    """Summary
        Display help messages
    Args:
        bot (TYPE): The bot, always good to send
        update (TYPE): the message handler
        args (TYPE): Description
    Returns:
        TYPE: Description
    """
    if not args:
        update.message.reply_text(helpmessages.mainHelp())
    elif args[0] == "alert":
        bot.sendMessage(update.message.chat_id, helpmessages.alertHelp())
    elif args[0] == "fortune":
        bot.sendMessage(update.message.chat_id, fortune.fortuneHelp())
    elif args[0] == "quote":
        bot.sendMessage(update.message.chat_id, helpmessages.quoteHelp())
    elif args[0] == "bash":
        bot.sendMessage(update.message.chat_id, helpmessages.bashHelp())
    else:
        update.message.reply_text(helpmessages.mainHelp())


def madcow(bot, update):
    """Summary
    Displays an offensive fortune, within a dead cow
    Args:
        bot (TYPE): The bot, always good to send
        update (TYPE): the message handler
    """
    frt = fortune.fortune("off")
    message = fortune.madcow([frt])
    message = message.replace("<", "&lt;")
    message = message.replace(">", "&gt;")
    bot.sendMessage(update.message.chat_id, text="<code>" + message + "</code>",
                    parse_mode=telegram.ParseMode.HTML)


def get_cowsay(bot, update, args):
    """Summary
    Displays a cow with either a fortune or a user provided message
    Args:
        bot (TYPE): The bot, always good to send
        update (TYPE): the message handler
        args (TYPE): Description
    """
    args = ' '.join(args)
    if not args:
        frt = fortune.fortune(args)
    else:
        frt = args
    message = fortune.cowsay([frt])
    message = message.replace("<", "&lt;")
    message = message.replace(">", "&gt;")
    bot.sendMessage(update.message.chat_id, text="<code>" + message + "</code>",
                    parse_mode=telegram.ParseMode.HTML)


def get_fortune(bot, update, args):
    """Summary
    Gets a fortune
    Args:
        bot (TYPE): The bot, always good to send
        update (TYPE): the message handler
        args (TYPE): Description
    """
    args = ' '.join(args)
    bot.sendMessage(update.message.chat_id, fortune.fortune(args))


def get_eight_ball(bot, update, args):
    """Summary

    Args:
        bot (TYPE): The bot, always good to send
        update (TYPE): the message handler
        args (TYPE): Description
    """
    args = ' '.join(args)
    bot.sendMessage(update.message.chat_id,
                    "Give me a few seconds to ponder this...")
    bot.sendMessage(update.message.chat_id, eightBall.isQuestion(args))


def pong(bot, update):
    """Summary

    Args:
        bot (TYPE): The bot, always good to send
        update (TYPE): the message handler
    """
    update.message.reply_text("pong")


def echo(bot, update):
    """Summary

    Args:
        bot (TYPE): The bot, always good to send
        update (TYPE): the message handler
    """
    update.message.reply_text(update.message.text)


def alarm(bot, job):
    """Function to send the alarm message

    Args:
        bot (TYPE): The bot, always good to send
        update (TYPE): the message handler
    """
    message = MESSAGES[job.context]
    if len(message) <= 0:
        message = "Alert set for right now"
    bot.sendMessage(job.context, text=message)


def alert(bot, update, args, job_queue):
    """Adds a job to the queue

    Args:
        bot (TYPE): The bot, always good to send
        update (TYPE): the message handler
        args (TYPE): Description
        job_queue (TYPE): Description

    Returns:
        TYPE: Description
    """
    continue_on = 1
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    user = str(update.message.from_user)
    if not args:
        update.message.reply_text('please enter a time')
        return
    if '|' in args:
        message = ' '.join(args)
        argstemp = message.split('|')
        due = alerts.lastDitchAttempt(argstemp[0])
        if due > 0:
            argstemp.pop(0)
            message = ' '.join(argstemp)
            continue_on = -1
    if continue_on == 1:
        due = alerts.parseADate(args[0])
        if due <= 0:
            due = alerts.regexmatch(args[0])
        args.pop(0)
        message = ' '.join(args)
        if due <= 0:
            update.message.reply_text('Sorry that is not a valid time')
            return

    # Add job to queue
    my_context = '' + str(chat_id) + ':' + str(message_id)
    job = Job(alarm, due, repeat=False, context=my_context)
    USERS[my_context] = user
    MESSAGES[my_context] = message
    TIMERS[my_context] = job
    job_queue.run_once(alarm, due, context=my_context)
    current_time = datetime.now()
    due = int((current_time - datetime(1970, 1, 1)).total_seconds() + due)
    fileIO.writeAlertJob("alerts", str(chat_id),
                         str(message_id), user, due, message)
    set_for = alerts.timeSetFor(due)
    bot.sendMessage(update.message.chat_id, 'Timer successfully set for: ' + str(set_for) +
                    '\nYour ID is:' + str(message_id))


def get_dilbert(bot, update, args):
    """Summary

    Args:
        bot (TYPE): The bot, always good to send
        update (TYPE): the message handler
        args (TYPE): Description
    """
    dilbert_strip = dilbert.getStrip()
    bot.sendMessage(update.message.chat_id, dilbert_strip)


def get_xkcd(bot, update, args):
    """Summary

    Args:
        bot (TYPE): The bot, always good to send
        update (TYPE): the message handler
        args (TYPE): Description
    """
    if not args:
        xkcd_url = xkcd.getStrip()
    else:
        xkcd_number = ' '.join(args)
        xkcd_url = xkcd.getStrip(xkcd_number)
    bot.sendMessage(update.message.chat_id, xkcd_url)


def set_quote(bot, update, args):
    """Summary

    Args:
        bot (TYPE): The bot, always good to send
        update (TYPE): the message handler
        args (TYPE): Description
    """
    chat_file = str(update.message.chat_id)
    user = str(update.message.from_user)
    message = ' '.join(args)
    response = fileIO.WriteAQuote(chat_file, message, user)
    bot.sendMessage(update.message.chat_id, response)


def remove_quote(bot, update, args):
    """Summary

    Args:
        bot (TYPE): The bot, always good to send
        update (TYPE): the message handler
        args (TYPE): Description
    """
    chat_file = str(update.message.chat_id)
    user = str(update.message.from_user)
    quote_id = args[0]
    response = fileIO.removeQuote(chat_file, quote_id, user)
    update.message.reply_text(response)


def get_quote(bot, update, args):
    """Summary

    Args:
        bot (TYPE): The bot, always good to send
        update (TYPE): the message handler
        args (TYPE): Description
    """
    chat_file = str(update.message.chat_id)
    if not args:
        response = fileIO.getRandQuote(chat_file)
    else:
        quote_id = args[0]
        response = fileIO.getQuote(chat_file, quote_id)
    update.message.reply_text(response)


def remove(bot, update, args):
    """Removes the job if the user changed their mind

    Args:
        bot (TYPE): The bot, always good to send
        update (TYPE): the message handler
        args (TYPE): Description

    Returns:
        TYPE: Description
    """
    try:
        my_context_id = ''.join(args)
        my_context = str(update.message.chat_id) + ':' + my_context_id
        user = str(update.message.from_user)
        if my_context not in TIMERS:
            update.message.reply_text(
                'You have no active timer with code:' + my_context_id)
            return
        if user != USERS[my_context]:
            update.message.reply_text("You did not enter that alert!")
            return
        job = TIMERS[my_context]
        job.schedule_removal()
        del TIMERS[my_context]
        del MESSAGES[my_context]
        del USERS[my_context]
        bot.sendMessage(update.message.chat_id, 'Timer successfully removed! Removed message id: ' +
                        my_context_id)

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /alert <seconds>')


def bot_error(bot, update, error):
    """Summary

    Args:
        bot (TYPE): The bot, always good to send
        update (TYPE): the message handler
        error (TYPE): Description
    """
    print LOGGER.warn('Update %s caused error %s', update, error)


def find_existing_alerts(job_queue):
    """Summary

    Args:
        job_queue (TYPE): Description
    """
    try:
        my_jobs = fileIO.readJobs("alerts")
        t = datetime.now()
        if my_jobs != 0:
            for job in my_jobs:
                due = int(job.due) - \
                    int((t - datetime(1970, 1, 1)).total_seconds())
                if due > 0:
                    my_context = '' + str(job.chatId) + \
                        ':' + str(job.messageId)
                    my_job = Job(alarm, due, repeat=False, context=my_context)
                    USERS[my_context] = job.user
                    MESSAGES[my_context] = job.message
                    TIMERS[my_context] = my_job
                    job_queue.put(my_job)
                    fileIO.writeAlertJob("alerts", job.chatId, job.messageId, job.user, job.due,
                                         job.message)
    except:
        print ("Unexpected error:", sys.exc_info())


def choice(bot, update, args):
    """Summary

    Args:
        bot (TYPE): The bot, always good to send
        update (TYPE): the message handler
        args (TYPE): Description
    """
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
    # update.message.reply_text(random.choice(sec))


def parse_message(bot, update):
    """Summary

    Args:
        bot (TYPE): The bot, always good to send
        update (TYPE): the message handler
    """
    strings = update.message.text.split()
    subreddit_match = re.compile('^(/r/)')
    reddit_base = "https://www.reddit.com"
    for word in strings:
        if re.match(subreddit_match, word):
            subreddit = reddit_base + word
            if len(word) > 3:
                bot.sendMessage(update.message.chat_id, subreddit)
            # update.message.reply_text(subreddit)


def get_bash_quotes(bot, update, args):
    """Summary

    Args:
        bot (TYPE): The bot, always good to send
        update (TYPE): the message handler
        args (TYPE): Description
    """
    if not args == 0:
        bash_quote = bashQuotes.getPost()
    else:
        specific_quote_num = ' '.join(args)
        bash_quote = bashQuotes.getPost(specific_quote_num)
    bot.sendMessage(update.message.chat_id, bash_quote)


def notify_xkcd(bot, update, args):
    """Summary

    Args:
        bot (TYPE): The bot, always good to send
        update (TYPE): the message handler
        args (TYPE): Description
    """
    if not args:
        my_message = xkcd.AddChatId(update.message.chat_id)
    elif args[0] == "remove":
        my_message = xkcd.RemoveChatId(update.message.chat_id)
    else:
        my_message = "That was not a valid command"
    bot.sendMessage(update.message.chat_id, my_message)


def check_latest_xkcd(bot, job):
    """Summary

    Args:
        bot (TYPE): Description
        job (TYPE): Description

    Returns:
        TYPE: Description
    """
    new_comic = xkcd.sendLatest()
    if new_comic == '':
        return
    else:
        chat_ids = xkcd.GetChatIds()
        for chat_id in chat_ids:
            bot.sendMessage(chat_id, new_comic)

def notify_motorcyle(bot, update, args):
    """Summary

    Args:
        bot (TYPE): The bot, always good to send
        update (TYPE): the message handler
        args (TYPE): Description
    """
    if not args:
        my_message = motorcycleUpdates.AddChatId(update.message.chat_id)
    elif args[0] == "remove":
        my_message = motorcycleUpdates.RemoveChatId(update.message.chat_id)
    else:
        my_message = "That was not a valid command"
    bot.sendMessage(update.message.chat_id, my_message)


def check_latest_motorcycle(bot, job):
    """Summary

    Args:
        bot (TYPE): Description
        job (TYPE): Description

    Returns:
        TYPE: Description
    """
    chat_ids = motorcycleUpdates.GetChatIds()
    motrcycleValue = motorcycleUpdates.getCount()
    if motrcycleValue == 3:
        return ""
    else:
        for chat_id in chat_ids:
            bot.sendMessage(chat_id, motrcycleValue)


def main():
    """Summary
    """
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(MYTOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", bot_help, pass_args=True))
    dispatcher.add_handler(CommandHandler(
        "fortune", get_fortune, pass_args=True))
    dispatcher.add_handler(CommandHandler(
        "cowsay", get_cowsay, pass_args=True))
    dispatcher.add_handler(CommandHandler("ping", pong))
    dispatcher.add_handler(CommandHandler("madcow", madcow))
    dispatcher.add_handler(CommandHandler(
        "alert", alert, pass_args=True, pass_job_queue=True))
    dispatcher.add_handler(CommandHandler("remove", remove, pass_args=True))
    dispatcher.add_handler(CommandHandler("choose", choice, pass_args=True))
    # Quote functions
    dispatcher.add_handler(CommandHandler(
        "setquote", set_quote, pass_args=True))
    dispatcher.add_handler(CommandHandler(
        "removequote", remove_quote, pass_args=True))
    dispatcher.add_handler(CommandHandler("quote", get_quote, pass_args=True))
    dispatcher.add_handler(CommandHandler(
        "dilbert", get_dilbert, pass_args=True))
    dispatcher.add_handler(CommandHandler("xkcd", get_xkcd, pass_args=True))
    dispatcher.add_handler(CommandHandler(
        "notifyxkcd", notify_xkcd, pass_args=True))
    dispatcher.add_handler(CommandHandler(
        "notifymotorcycle", notify_motorcyle, pass_args=True))
    dispatcher.add_handler(CommandHandler(
        "bash", get_bash_quotes, pass_args=True))
    dispatcher.add_handler(CommandHandler(
        "8ball", get_eight_ball, pass_args=True))
    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler([Filters.text], parse_message))

    # log all errors
    dispatcher.add_error_handler(bot_error)

    # Start the Bot
    find_existing_alerts(updater.job_queue)
    xkcd.ReadLatestFromFile()
    xkcd.getLatests()
    #myJob = Job(checkLatestxkcd, 900, repeat=True, context="my_context")
    updater.job_queue.run_repeating(
        check_latest_xkcd, interval=900, first=0, context="my_context")
    updater.job_queue.run_repeating(
        check_latest_motorcycle, interval=3600, first=0, context="my_context")
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
