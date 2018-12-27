import os
from telegram.ext import Updater, MessageHandler, Filters


# add handlers

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)



if __name__ == '__main__':
    TOKEN = os.environ.get('TOKEN', '')
    PORT = int(os.environ.get('PORT', '8443'))
    updater = Updater(TOKEN)
    echo_handler = MessageHandler(Filters.text, echo)
    updater.dispatcher.add_handler(echo_handler, group=1)

    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.set_webhook("https://66fa704b.ngrok.io/" + TOKEN)
    updater.idle()

