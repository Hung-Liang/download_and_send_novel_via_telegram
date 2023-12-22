from lib.tools.json_handler import check_book, add_book, add_website
from lib.helper.telegram_helper import TelegramHelper
from pathlib import Path
from lib.tools.tools import (
    get_fid,
    check_progress,
    delete_dir,
    get_bot_message,
)
from lib.tools.crawler_handler import select_crawler
import threading


def master_handler(cid, url: str, bot=None, redownload=False):
    """Master handler of the bot.

    Args:
        `cid`: The chat id of the user.
        `url`: The url of the novel.
        `bot`: The bot object.
        `redownload`: Redownload the novel.
    """

    crawler, website = select_crawler(url)

    if bot and not crawler:
        bot.message.reply_text("網址不支援")
        return

    title = crawler.title
    author = crawler.author

    chapter_size = crawler.chapter_size
    destination_path = crawler.path

    book_exist, website_exist, length_match, fid = check_book(
        title, website, chapter_size
    )

    telegram_helper = TelegramHelper()

    if redownload:
        bot_message = "重新下載<b>{}</b>網站版本的<b>{}</b>".format(website, title)
        book_exist, website_exist, length_match = True, False, False

    else:
        bot_message = get_bot_message(
            book_exist, website_exist, length_match, title, website
        )

    if bot:
        message = bot.message.reply_text(
            bot_message,
            parse_mode="HTML",
        )

    if length_match:
        telegram_helper.send_document_by_fid(cid, fid)
        return

    if not book_exist:
        add_book(title, author)

    progress_thread = threading.Thread(
        target=check_progress,
        args=(title, website, destination_path, chapter_size, bot, message),
    )
    progress_thread.start()

    crawler.download()

    progress_thread.join()

    file_name = "{}.txt".format(title)
    file_path = Path(destination_path, file_name)

    success, res = telegram_helper.send_document(
        cid, file_path, "[{}] {}".format(website, file_name)
    )

    delete_dir(destination_path)

    if success:
        add_website(
            title,
            website,
            url,
            get_fid(res),
            chapter_size,
        )
        if bot:
            message.edit_text("<b>{}</b>傳送成功".format(title), parse_mode="HTML")
    else:
        if bot:
            message.edit_text("<b>{}</b>傳送失敗".format(title), parse_mode="HTML")
