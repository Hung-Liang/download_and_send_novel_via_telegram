import os
from telegram.ext import Updater, CommandHandler
from lib.distributer import distributer

from dotenv import load_dotenv

load_dotenv()


def download(bot, update):
    url = str(bot.message['text'].replace('/d ', '').strip())
    cid = bot.message.from_user.id
    distributer(cid, url, bot)


# def download(bot, update):
#     url = bot.message['text'].replace('/d ', '').strip()
#     uid = bot.message.from_user.id
#     sendFileHandler(uid, url, bot)


# def redownload(bot, update):
#     uid = bot.message.from_user.id
#     msg = bot.message['text'].replace('/redownload ', '').strip()

#     url = remove_and_get_url(bot, msg)

#     if url != None:
#         sendFileHandler(uid, url, bot)


# def resend(bot, update):
#     uid = bot.message.from_user.id
#     msg = bot.message['text'].replace('/resend ', '').strip()
#     if msg != '/resend':
#         find_book(bot, uid, msg)
#     else:
#         send_all(uid)
#         bot.message.reply_text('重新傳送全部書本完畢')


# def books(bot, update):
#     uid = bot.message.from_user.id
#     bot.message.reply_text('以下為現有的書')
#     get_books_name(uid)


# def help(bot, update):
#     bot.message.reply_text(
#         '/d 下載\n/resend 重新傳送\n/books 所有的書名\n/redownload 重新下載\n'
#     )


# def shutdown():
#     updater.stop()
#     updater.is_idle = False


# def stop(bot, update):
#     uid = bot.message.from_user.id
#     if str(uid) == os.environ.get("admin_id"):
#         bot.message.reply_text('Bot Shutting Down')
#         threading.Thread(target=shutdown).start()
#     else:
#         bot.message.reply_text('You do not have permission')


# getEverythingReady()


# updater.dispatcher.add_handler(CommandHandler('resend', resend))
# updater.dispatcher.add_handler(CommandHandler('books', books))
# updater.dispatcher.add_handler(CommandHandler('redownload', redownload))
# updater.dispatcher.add_handler(CommandHandler('help', help))
# updater.dispatcher.add_handler(CommandHandler('stop', stop))

updater = Updater(os.environ.get("tg_token"))

updater.dispatcher.add_handler(CommandHandler('d', download))

updater.start_polling()
updater.idle()
