import requests
import os
import json
from dotenv import load_dotenv
from lib.utils.logger import log

load_dotenv()


class TelegramHelper:
    """Telegram Helper

    Attributes:
        `token`: Telegram Bot Token.

    Functions:
        `send_message`: Send message to Telegram.
        `send_document`: Send document to Telegram.
        `send_document_by_fid`: Send document by file id to Telegram.
    """

    def __init__(self):
        self.token = os.environ.get("tg_token")

    def send_message(self, cid, message):
        """Send message to Telegram.

        Args:
            `cid`: Chat ID.
            `message`: Message to send.

        Returns:
            True if success, False if fail.
        """

        url = (
            'https://api.telegram.org/bot{}'
            '/sendMessage?chat_id={}&parse_mode=HTML&text={}'.format(
                self.token, cid, message
            )
        )

        res = requests.get(url)

        log(
            '[telegram_lib]',
            f'send message: {res.status_code} {res.text}',
        )

        if res.status_code == 200:
            return True
        else:
            return False

    def send_document(self, cid, path, filename):
        """Send document to Telegram.

        Args:
            `cid`: Chat ID.
            `path`: Path to file.
            `filename`: Filename.

        Returns:
            True if success, False if fail.
        """
        files = {
            "document": (
                filename,
                open(path, 'rb'),
                'application/octet-stream',
            ),
        }
        url = 'https://api.telegram.org/bot{}/sendDocument?chat_id={}'.format(
            self.token, cid
        )

        res = requests.post(url, files=files)

        log(
            '[telegram_lib]',
            f'send document: {res.status_code} {res.text}',
        )

        if res.status_code == 200:
            return True, json.loads(res.text)
        else:
            return False, json.loads(res.text)

    def send_document_by_fid(self, cid, fid):
        """Send document by file id to Telegram.

        Args:
            `cid`: Chat ID.
            `fid`: File ID.

        Returns:
            True if success, False if fail.
        """

        url = (
            'https://api.telegram.org/bot{}'
            '/sendDocument?chat_id={}&document={}'.format(self.token, cid, fid)
        )

        res = requests.post(url)

        log(
            '[telegram_lib]',
            f'send document by fid: {res.status_code} {res.text}',
        )

        if res.status_code == 200:
            return True
        else:
            return False
