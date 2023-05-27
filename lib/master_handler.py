from lib.tools.json_handler import check_book, add_book, add_website
from lib.tools.telegram_helper import TelegramHelper
from lib.tools.tools import start_download
from pathlib import Path
from lib.tools.tools import (
    get_fid,
    progress_check,
    delete_dir,
    get_bot_message,
)
from lib.tools.crawler_handler import select_crawler


def master_handler(cid, url: str, bot=None, redownload=False):

    crawler, website, crawler_path = select_crawler(url)

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
        book_exist, website_exist, length_match = False, False, False

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

    start_download(crawler_path, url)

    file_name = "{}.txt".format(title)
    file_path = Path(destination_path, file_name)

    previous_size = 0

    while True:

        finished, previous_size, current_size = progress_check(
            destination_path, previous_size, chapter_size
        )
        if finished:
            if bot:
                message.edit_text(
                    "<b>{}</b>網站版本的<b>{}</b>下載完成，正在傳送".format(website, title)
                )
            break
        else:
            if bot:
                try:
                    message.edit_text(
                        "<b>{}</b>網站版本的<b>{}</b>下載中，進度：{}/{}".format(
                            website, title, current_size, chapter_size
                        ),
                        parse_mode="HTML",
                    )
                except Exception:
                    pass

    success, res = telegram_helper.send_document(cid, file_path, file_name)

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
