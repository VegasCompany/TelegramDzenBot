#!/usr/bin/env python
# -*- coding: utf-8 -*-


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import requests
import urllib.request
from bs4 import BeautifulSoup

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! Я помогу тебе оперативно смотреть, сколько просмотров, дочиток на твоей статье. Пришли ссылку на статью.')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Отправь мне ссылку на статью')

class Parse:
	def __init__(self, url):
		self.html = urllib.request.urlopen(url).read()
		self.start()

	def start(self):
		soup = BeautifulSoup(self.html, 'lxml')

		date = soup.find('span', class_='article-stat__date').get_text()
		print(date)

def echo(bot, update):
    """Echo the user message."""
    ssilka = update.message.text
    print(ssilka)
    bot = Bot_Dzen(ssilka)
    update.message.reply_text('Анализирую..')
    update.message.reply_text(views)
class Bot_Dzen:
	def __init__(self, link_artical):
		self.url = link_artical
		self.data = None
		self.parse()

	def state(self, respons):
		for key, value in respons.items():
			if key == 'views':
				views = value
			if key == 'viewsTillEnd':
				viewsTillEnd = value
		print(viewsTillEnd)
		p = Parse(self.url)

	def json_url(self, new_url):
		request = requests.get('https://zen.yandex.ru/media-api/publication-view-stat?publicationId=%s'%(new_url), params=self.data)
		respons = request.json()
		self.state(respons)
	def parse(self):

		url_parse = self.url.split("/")[6]
		new_parse = url_parse.split('-')[-1]

		self.json_url(new_parse)





def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("557212771:AAFnYsNajih707BkQFxq7HLwiI8vUPb7lU0")

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
