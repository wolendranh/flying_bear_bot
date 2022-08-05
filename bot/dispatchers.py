import logging
import re

from telegram.ext import CommandHandler, Dispatcher, CallbackContext
from telegram import Bot, Update

from .services import (
    get_random_quote_by_tag, get_random_quote, store_quote, get_keyword_quote_count,
    get_stream_list_by_game
)

logger = logging.getLogger(__name__)
# for dev env
# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def help(bot: Bot, update: Update):
    bot.sendMessage(update.message.chat_id, text="""
                         reply message and add  /keyword or /k after with stop word to create stop word -> quote relation.\n 
                         - /random or /r - show random quote \n
                         - /count or /c - show random quote \n
                         - /st or /stream - following game name (/st dota2) to retrieve top streams (NEW) \n                               
                         """
                    )


def error(bot: Bot, update: Update, error_text: str = 'Command not found .'):
    bot.sendMessage(update.message.chat_id, text=error_text)


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


# def snow_camera(bot: Bot, update: Update):
#     location = re.sub(r'/[camera|cam]+', '', update.message.text).strip().lower()
#
#     try:
#         location_obj = Location.objects.get(Q(title_en__iexact=location) | Q(title_uk__iexact=location))
#     except Location.DoesNotExist:
#         error(bot, update,
#               "Location is not supported yet.")
#         return
#
#     cameras_map = location_obj.cameras.values_list("title_uk", "cam_id")
#
#     button_list = [
#         InlineKeyboardButton(camera[0], callback_data=f"cam={camera[1]}")
#         for camera in cameras_map
#     ]
#
#     reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
#     bot.send_message(chat_id=update.message.chat_id, text="Please select camera", reply_markup=reply_markup)
#

# def snow_camera_gif(bot: Bot, update: Update):
#     location = re.sub(r'/[camera_vid|camv]+', '', update.message.text).strip().lower()
#
#     try:
#         location_obj = Location.objects.get(Q(title_en__iexact=location) | Q(title_uk__iexact=location))
#     except Location.DoesNotExist:
#         error(bot, update,
#               "Location is not supported yet.")
#         return
#
#     cameras_map = location_obj.cameras.values_list("title_uk", "cam_id")
#
#     button_list = [
#         InlineKeyboardButton(camera[0], callback_data=f"camv={camera[1]}")
#         for camera in cameras_map
#     ]
#
#     reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
#     bot.send_message(chat_id=update.message.chat_id, text="Please select camera", reply_markup=reply_markup)
#
#
# def weather(bot: Bot, update: Update):
#     try:
#         city = re.sub(r'/[weather|w]+', '', update.message.text).strip()
#         weather = get_weather(city=city)
#         bot.sendMessage(update.message.chat_id, text=weather)
#     except Exception as e:
#         logger.exception('Failed to get weather. Error', exc_info=e)


def quote(update: Update, context: CallbackContext):
    try:
        text, author = update.message.reply_to_message.text, update.message.reply_to_message.from_user.full_name
        stripped_stop_word = re.sub(r'/[store|s]+', '', update.message.text).strip()
        if stripped_stop_word:
            store_quote(text=text, author=author, tag_text=stripped_stop_word)
            context.bot.sendMessage(update.message.chat_id, text='I stored your quote from {}!'.format(author))
        else:
            context.bot.sendMessage(update.message.chat_id,
                            text='Stop word missing. Please provide stop word text after `/store` command! Thanks!')
    except Exception as e:
        logger.exception('Failed to store quote. Error', exc_info=e)
        

def random_by_stop_word(update: Update, context: CallbackContext):
    quote = get_random_quote_by_tag(message_text=update.message.text)
    context.bot.send_message(chat_id=update.message.chat_id, text=quote, parse_mode='HTML')


def random(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id, text=get_random_quote(), parse_mode='HTML')


def quote_count_by_keyword(update: Update, context: CallbackContext):
    try:
        keyword = re.sub(r'/[count|c]+', "", update.message.text).strip()
        message = get_keyword_quote_count(keyword=keyword)
        context.bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode='HTML')
    except Exception as e:
        logger.exception('Failed to get count for keyword.', exc_info=e)


def get_streams_by_game(bot: Bot, update: Update):
    try:
        game = re.sub(r'/[stream|st]+', "", update.message.text).strip()

        message = get_stream_list_by_game(game_name=game)
        bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode='HTML')
    except Exception as e:
        bot.sendMessage(update.message.chat_id,
                        text='There are no streams or game name was not specific enough.')
        logger.exception('Failed to get count for keyword.', exc_info=e)


def register(dispatcher: Dispatcher):
    """
    this method will be called on start of application
    and register bot callbacks
    """
    # quotes
    dispatcher.add_handler(CommandHandler(["store", "s"], quote))
    dispatcher.add_handler(CommandHandler(["random", "r"], random))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler(["keyword", "k"], random_by_stop_word))
    dispatcher.add_handler(CommandHandler(["count", "c"], quote_count_by_keyword))
    # dispatcher.add_handler(CommandHandler(["weather", "w"], weather))
    # dispatcher.add_handler(CallbackQueryHandler(camera_handler, pattern="^cam=\d+$"))
    # dispatcher.add_handler(CallbackQueryHandler(camera_handler, pattern="^camv=\d+$"))

    # twitch
    # not needed for now
    # dispatcher.add_handler(CommandHandler(["stream", "st"], get_streams_by_game))

    # snow cameras
    # dispatcher.add_handler(CommandHandler(["camera", "cam"], snow_camera))
    # dispatcher.add_handler(CommandHandler(["camera_gif", "camv"], snow_camera_gif))

    # TODO: make this react to messages with some sane timeout, e.g. sent msg from bot not more then 20 in day
    # dispatcher.add_handler(MessageHandler(Filters.text, random_by_stop_word), group=1)
    # dispatcher.add_error_handler(error)
