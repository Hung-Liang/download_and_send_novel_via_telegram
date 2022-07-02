import os
from telegram.ext import Updater, CommandHandler
from lib.common import sendFileHandler, getEverythingReady
import threading
from dotenv import load_dotenv
load_dotenv()

def download(bot, update):
    url=bot.message['text'].replace('/d ','')
    uid=bot.message.from_user.id
    sendFileHandler(uid,url,bot)

def shutdown():
    updater.stop()
    updater.is_idle = False

def stop(bot, update):
    uid=bot.message.from_user.id
    if str(uid)==os.environ.get("admin_id"):
        bot.message.reply_text('Bot Shutting Down')
        threading.Thread(target=shutdown).start()
    else:
        bot.message.reply_text('You do not have permission')

getEverythingReady()

updater = Updater(os.environ.get("tg_token"))

updater.dispatcher.add_handler(CommandHandler('d', download))
updater.dispatcher.add_handler(CommandHandler('stop', stop))

updater.start_polling()
updater.idle()