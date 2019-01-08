import logging

from telegram.ext import CommandHandler, Filters, MessageHandler, Dispatcher
from telegram import Bot

from .services import get_random_quote_by_stop_word, get_random_quote, store_quote

logger = logging.getLogger(__name__)


def help(bot: Bot, update: dict):
    bot.sendMessage(update.message.chat_id, text="""
                         - reply message and add /keyword after with stop word to create stop word -> quote relation. \n- /random - show random quote                            
                         """
                    )


def error(bot: Bot, update: dict):
    bot.sendMessage(update.message.chat_id, text='Command not found .')

def quote(bot: Bot, update: dict):
    try:
        text, author = update.message.reply_to_message.text, update.message.reply_to_message.from_user.full_name
        stripped_stop_word = update.message.text.replace('/keyword', '').strip()
        if stripped_stop_word:
            store_quote(text=text, author=author, stop_word_text=stripped_stop_word)
            bot.sendMessage(update.message.chat_id, text='I stored your quote from {}!'.format(author))
        else:
            bot.sendMessage(update.message.chat_id,
                            text='Stop word missing. Please provide stop word text after `/keyword` command! Thanks!')
    except Exception as e:
        logger.exception('Failed to store quote. Error', exc_info=e)
        

def random_by_stop_word(bot: Bot, update: dict):
    quote = get_random_quote_by_stop_word(message_text=update.message.text) 
    bot.send_message(chat_id=update.message.chat_id, text=quote)


def random(bot: Bot, update: dict):
    bot.send_message(chat_id=update.message.chat_id, text=get_random_quote(), parse_mode='HTML')


def register(dispatcher: Dispatcher):
    """
    this method will be called on start of application
    and register bot callbacks
    """
    dispatcher.add_handler(CommandHandler("keyword", quote))
    dispatcher.add_handler(CommandHandler("random", random))
    dispatcher.add_handler(CommandHandler("help", help))

    dispatcher.add_handler(MessageHandler(Filters.text, random_by_stop_word), group=1)
    dispatcher.add_error_handler(error)