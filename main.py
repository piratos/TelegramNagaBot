from uuid import uuid4

import logging
import requests
import json
import re

import creds

from telegram.utils.helpers import escape_markdown
from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler



# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


TICKERURL = 'https://api.hitbtc.com/api/2/public/ticker/ngcusd'

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

def get_naga():
    r = requests.get(TICKERURL)
    data = json.loads(r.text)
    return 'BID: {}\nASK: {}\nLAST: {}\nHIGH: {}\nLOW: {}\nVOL: {}'.format(data['bid'],
                                                                           data['ask'],
                                                                           data['last'],
                                                                           data['high'],
                                                                           data['low'],
                                                                           data['volume'])
def naga(bot, update):
    update.message.reply_text(get_naga())


def inlinequery(bot, update):
    """Handle the inline query."""
    data = get_naga()
    query = update.inline_query.query
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="NAGA TICKER",
            input_message_content=InputTextMessageContent(
                data)),]

    update.inline_query.answer(results, cache_time=0)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(creds.token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler('hello', hello))
    dp.add_handler(CommandHandler('naga', naga))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(inlinequery))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()