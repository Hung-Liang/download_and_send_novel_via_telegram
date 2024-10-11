from lib.helper.telegram_helper import TelegramHelper
from dotenv import load_dotenv
import os
from lib.utils.file_path import TEMP_PATH
from pathlib import Path
from lib.tools.json_handler import add_website
from lib.tools.tools import get_fid


load_dotenv()

book_name = "我本無意成仙"

book_path = Path(TEMP_PATH, book_name + ".txt")


telegram_helper = TelegramHelper()

website = "manually"

success, res = telegram_helper.send_document(
    os.environ.get("admin_id"),
    book_path,
    "[{}] {}".format(website, book_path.name),
)


if success:
    add_website(
        book_name,
        website,
        None,
        get_fid(res),
        None,
    )
