from pathlib import Path

from lib.utils.file_path import LOG_PATH
from datetime import datetime


def log(*messages, console: bool = False):
    """Basic Log to Record Progress.

    Args:
        `messages`: Logging message.
    """

    today = datetime.now().strftime('%Y-%m-%d') + '.log'

    file_path = Path(LOG_PATH, today)

    with open(file_path, 'a', encoding='utf-8') as f:
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), *messages, file=f)

    if console:
        print(messages)
