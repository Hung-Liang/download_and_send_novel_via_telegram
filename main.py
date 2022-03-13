import os
from telegram.ext import Updater, CommandHandler
from lib.common import sendFileHandler
from dotenv import load_dotenv
load_dotenv()

def download(bot, update):
    url=bot.message['text'].replace('/d ','')
    uid=bot.message.from_user.id
    sendFileHandler(uid,url,bot)

updater = Updater(os.environ.get("tg_token"))

updater.dispatcher.add_handler(CommandHandler('d', download))

updater.start_polling()
updater.idle()