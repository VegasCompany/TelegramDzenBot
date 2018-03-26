#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Bot to reply to Telegram messages.
This program is dedicated to the public domain under the CC0 license.
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import requests
import urllib.request
from bs4 import BeautifulSoup

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class Parse:
    def __init__(self, url):
        self.html = urllib.request.urlopen(url).read()
        self.start()

    def start(self):
        soup = BeautifulSoup(self.html, 'lxml')

        self.date = soup.find('span', class_='article-stat__date').get_text()
        print(self.date)

class Bot_Dzen:
    def __init__(self, link_artical):
        self.url = link_artical
        self.data = None
        self.parse()

    def state(self, respons):
        for key, value in respons.items():
            if key == 'views':
                self.views = value
            if key == 'viewsTillEnd':
                self.viewsTillEnd = value
        print(self.views)
        print(self.viewsTillEnd)
        #p = Parse(self.url)

    def json_url(self, new_url):
        request = requests.get('https://zen.yandex.ru/media-api/publication-view-stat?publicationId=%s'%(new_url), params=self.data)
        respons = request.json()
        self.state(respons)
    def parse(self):
        
        url_parse = self.url
        new_parse = url_parse[-24:]
        print(new_parse)

        self.json_url(new_parse)
# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Привет. Пришли ссылку на свою статью.')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Пришли ссылку на свою статью.')


def echo(bot, update):
    """Echo the user message."""
    ssilka = update.message.text
    if "https://zen." in ssilka or "http://zen." in ssilka:
        print(ssilka)
        bot = Bot_Dzen(ssilka)
        botdata = Parse(ssilka)
        prosmotrov = str(bot.views)
        dochitok = str(bot.viewsTillEnd)
        update.message.reply_text('Дата статьи ' + botdata.date + '\r\n' + 'Просмотров ' + prosmotrov + '\r\n' + 'Дочиток ' + dochitok)
    else:
        update.message.reply_text("Пришли ссылку на конкретную статью")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("532247434:AAEYKZ8bNmMIqQB7HRz1xkYrv-dQ_33RpPs")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()