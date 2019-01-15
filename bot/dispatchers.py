import logging
import re

from telegram.ext import CommandHandler, Filters, MessageHandler, Dispatcher
from telegram import Bot, Update

from .services import get_random_quote_by_stop_word, get_random_quote, store_quote

logger = logging.getLogger(__name__)


def help(bot: Bot, update: Update):
    bot.sendMessage(update.message.chat_id, text="""
                         - reply message and add /keyword after with stop word to create stop word -> quote relation. \n- /random - show random quote                            
                         """
                    )


def error(bot: Bot, update: Update):
    bot.sendMessage(update.message.chat_id, text='Command not found .')


def quote(bot: Bot, update: Update):
    try:
        text, author = update.message.reply_to_message.text, update.message.reply_to_message.from_user.full_name
        stripped_stop_word = re.sub(r'/[store|s]+', '', update.message.text).strip()
        if stripped_stop_word:
            store_quote(text=text, author=author, stop_word_text=stripped_stop_word)
            bot.sendMessage(update.message.chat_id, text='I stored your quote from {}!'.format(author))
        else:
            bot.sendMessage(update.message.chat_id,
                            text='Stop word missing. Please provide stop word text after `/store` command! Thanks!')
    except Exception as e:
        logger.exception('Failed to store quote. Error', exc_info=e)
        

def random_by_stop_word(bot: Bot, update: Update):
    quote = get_random_quote_by_stop_word(message_text=update.message.text) 
    bot.send_message(chat_id=update.message.chat_id, text=quote, parse_mode='HTML')


def random(bot: Bot, update: Update):
    bot.send_message(chat_id=update.message.chat_id, text=get_random_quote(), parse_mode='HTML')


def register(dispatcher: Dispatcher):
    """
    this method will be called on start of application
    and register bot callbacks
    """
    dispatcher.add_handler(CommandHandler(["store", "s"], quote))
    dispatcher.add_handler(CommandHandler(["random", "r"], random))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler(["keyword", "k"], random_by_stop_word))

    # TODO: make this react to messages with some sane timeout, e.g. sent msg from bot not more then 20 in day
    # dispatcher.add_handler(MessageHandler(Filters.text, random_by_stop_word), group=1)
    dispatcher.add_error_handler(error)
