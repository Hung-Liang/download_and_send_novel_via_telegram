import json
import os
import re
from pathlib import Path
from time import sleep

from lib.helper.telegram_helper import TelegramHelper
from lib.utils.file_path import CRAWLER_HANDLER_PATH


def load_json(path):
    """Load the json file.

    Args:
        `path`: The path of the json file.

    Returns:
        `data`: The data of the json file.
    """

    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path, data):
    """Save the data to the json file.

    Args:
        `path`: The path of the json file.
        `data`: The data of the json file.
    """

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_fid(res):
    """Get the file id from the response.

    Args:
        `res`: The response from the telegram api.

    Returns:
        `file_id`: The file id of the file.
    """

    return res['result']['document']['file_id']


def check_progress(
    title, website, destination_path, chapter_size, bot=None, message=None
):
    """Check the progress.

    Args:
        `path`: The path of the novel download file.

    Returns:
        True if the download is finished, False otherwise.

    """

    previous_size = 0
    death_counter = 0

    while True:

        finished, previous_size, current_size = number_of_file_check(
            destination_path, previous_size, chapter_size
        )
        if finished:
            if bot:
                message.edit_text(
                    "<b>{}</b>網站版本的<b>{}</b>下載完成，正在傳送".format(website, title),
                    parse_mode="HTML",
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
                    death_counter += 1
                    if death_counter == 30:
                        break


def delete_file(path):
    """Delete the file.

    Args:
        `path`: The path of the file.
    """

    path.unlink()


def delete_dir(path):
    """Delete the directory.

    Args:
        `path`: The path of the directory.
    """

    files = os.listdir(path)

    if len(files) != 0:
        for file in files:
            delete_file(Path(path, file))

    path.rmdir()


def get_bot_message(book_exist, website_exist, length_match, title, website):
    """Get the bot message.

    Args:
        `book_exist`: True if the book exist, False otherwise.
        `website_exist`: True if the website exist, False otherwise.
        `length_match`: True if the length match, False otherwise.
        `title`: The title of the novel.
        `website`: The website of the novel.

    Returns:
        `bot_message`: The bot message.
    """

    if book_exist and website_exist and length_match:
        bot_message = "<b>{}</b>網站版本的<b>{}</b>已存在，且沒有更新，正在傳送副本".format(
            website, title
        )

    elif book_exist and website_exist:
        bot_message = "<b>{}</b>網站版本的<b>{}</b>已存在，但有更新，正在重新下載".format(
            website, title
        )

    elif book_exist:
        bot_message = "<b>{}</b>已存在，但沒有<b>{}</b>網站版本，正在下載".format(
            title, website
        )

    else:
        bot_message = "<b>{}</b>不存在，正在下載<b>{}</b>網站版本".format(title, website)

    return bot_message


def number_of_file_check(path, previous_size, chapter_size):
    """Check the progress.

    Args:
        `path`: The path of the novel download file.

    Returns:
        True if the download is finished, False otherwise.

    """

    sleep(3)

    number_of_files = len(os.listdir(path))

    if number_of_files < chapter_size and number_of_files > previous_size:

        return False, number_of_files, number_of_files
    elif number_of_files < chapter_size and number_of_files < previous_size:

        return False, number_of_files, chapter_size
    elif number_of_files == 1:
        sleep(3)

        number_of_files = len(os.listdir(path))

        if number_of_files == 1:

            return True, number_of_files, chapter_size
        else:

            return False, number_of_files, number_of_files
    else:
        return False, chapter_size, chapter_size


def send_multiple_books(cid, fid_list):
    """Send multiple books to the user.

    Args:
        `cid`: The chat id of the user.
        `fid_list`: The list of file ids.
    """

    telegram_helper = TelegramHelper()

    for fid in fid_list:
        telegram_helper.send_document_by_fid(cid, fid)


def separate_message_for_telegram_limit(bulk_message):
    """Separate the message to fit the telegram limit.

    Args:
        `bulk_message`: The string of the message with multiple lines.

    Returns:
        The separated message in list.
    """

    lines = bulk_message.splitlines()

    messages = []
    message = ''

    for line in lines:
        if len(message) + len(line) <= 4096:
            message += line + '\n'

        else:
            messages.append(message)
            message = line + '\n'

    messages.append(message)
    return messages


def get_support_websites():
    """Get the support websites.

    Returns:
        `support_websites`: The support websites.
    """

    code = CRAWLER_HANDLER_PATH.read_text()
    urls = re.findall(r'url.startswith\(\'(https?://\S+)\'\)', code)

    return urls
