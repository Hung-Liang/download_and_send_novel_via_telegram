import os
from telegram.ext import Updater, CommandHandler
from lib.master_handler import master_handler
from lib.tools.json_handler import (
    get_websites,
    get_url,
    get_fid,
    get_all_fid,
    get_all_books_info,
)
from lib.tools.tools import (
    send_multiple_books,
    separate_message_for_telegram_limit,
    get_support_websites,
)
import threading
from lib.utils.logger import log
from dotenv import load_dotenv

load_dotenv()


def download(bot, update):
    url = str(bot.message['text'].replace('/d', '', 1).strip())
    cid = bot.message.from_user.id
    master_handler(cid, url, bot)


def multiple_download(bot, update):
    urls = bot.message['text'].replace('/md', '', 1).strip().split()
    cid = bot.message.from_user.id
    for url in urls:
        master_handler(cid, url, bot)


def support_website(bot, update):
    support_website = get_support_websites()
    support_website = '\n'.join(support_website)
    bot.message.reply_text('支援的網站有:\n{}'.format(support_website))


def redownload(bot, update):
    book_name = bot.message['text'].replace('/redownload', '').strip()
    cid = bot.message.from_user.id

    book_exist, websites = get_websites(book_name)

    if not book_exist:
        bot.message.reply_text('書本不存在')
        return
    for website in websites:

        url = get_url(book_name, website)

        try:
            master_handler(cid, url, bot, redownload=True)
        except Exception as e:
            bot.message.reply_text('{}網站版本的{}下載失敗'.format(website, book_name))
            log('[main]', 'Redownload error: ', e)


def resend(bot, update):
    cid = bot.message.from_user.id
    book_name = bot.message['text'].replace('/resend', '').strip()

    fid_list = []

    if book_name != '':
        book_exist, websites = get_websites(book_name)
        if not book_exist:
            bot.message.reply_text('書本不存在')
            return

        for website in websites:
            fid = get_fid(book_name, website)
            fid_list.append(fid)

    else:
        fid_list = get_all_fid()

    send_multiple_books(cid, fid_list)

    bot.message.reply_text('重新傳送全部書本完畢')


def books(bot, update):

    infos = get_all_books_info()
    bot.message.reply_text('以下為現有的書')

    messages = separate_message_for_telegram_limit(infos)
    for message in messages:
        bot.message.reply_text(message)


def help(bot, update):
    bot.message.reply_text(
        '/d 下載\n/md 下載多本書\n/resend 重新傳送\n/books 現有書單\n/redownload'
        ' 重新下載已知所有網站來源的特定書本\n/support 支援的網站\n/help 幫助\n'
    )


def stop(bot, update):
    uid = bot.message.from_user.id
    if str(uid) == os.environ.get("admin_id"):
        bot.message.reply_text('Bot Shutting Down')
        threading.Thread(target=shutdown).start()
    else:
        bot.message.reply_text('You do not have permission')


def shutdown():
    updater.stop()
    updater.is_idle = False


updater = Updater(os.environ.get("tg_token"))

updater.dispatcher.add_handler(CommandHandler('d', download))
updater.dispatcher.add_handler(CommandHandler('md', multiple_download))
updater.dispatcher.add_handler(CommandHandler('redownload', redownload))
updater.dispatcher.add_handler(CommandHandler('support', support_website))
updater.dispatcher.add_handler(CommandHandler('resend', resend))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('stop', stop))
updater.dispatcher.add_handler(CommandHandler('books', books))

updater.start_polling()
updater.idle()
