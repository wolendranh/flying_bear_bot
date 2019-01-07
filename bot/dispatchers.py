import logging

from telegram.ext import CommandHandler, Filters, MessageHandler

from .services import get_random_quote_by_stop_word, get_random_quote, store_quote

logger = logging.getLogger(__name__)


def help(bot, update):
    bot.sendMessage(update.message.chat_id, 
                    text="""
                         - reply message and add /quote after with stop word to create stop word -> quote relation  
                         - /random - show random quote 
                         """
                    )


def error(bot, update):
    bot.sendMessage(update.message.chat_id, text='Command not found .')


def quote(bot, update):
    try:
        text, author = update.message.reply_to_message.text, update.message.chat.first_name
        stripped_stop_word = update.message.text.replace('/quote', '').strip()
        if stripped_stop_word:
            store_quote(text=text, author=author, stop_word_text=stripped_stop_word)
            bot.sendMessage(update.message.chat_id, text='{}, I stored your quote!'.format(author))
        else:
            bot.sendMessage(update.message.chat_id,
                            text='Stop word missing. Please provide stop word text after `/quote` command! Thanks!')
    except Exception as e:
        logger.exception('Failed to store quote. Error', exc_info=e)
        

def random_by_stop_word(bot, update):
    quote = get_random_quote_by_stop_word(message_text=update.message.text) 
    bot.send_message(chat_id=update.message.chat_id, text=quote)


def random(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=get_random_quote())


# this method will be called on start of application
# and register bot callbacks
def register(dispatcher):
    dispatcher.add_handler(CommandHandler("quote", quote))
    dispatcher.add_handler(CommandHandler("random", random))
    dispatcher.add_handler(CommandHandler("help", help))

    dispatcher.add_handler(MessageHandler(Filters.text, random_by_stop_word), group=1)
    dispatcher.add_error_handler(error)