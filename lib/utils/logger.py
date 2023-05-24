from pathlib import Path

from lib.utils.file_path import LOG_PATH


def log(message: str = '', console: bool = False):
    '''Basic Log to Record Progress.

    Args:
        message: Logging message.
    '''

    file_path = Path(LOG_PATH, 'log.log')

    with open(file_path, 'a') as f:
        f.write(message + '\n')

    if console:
        print(message)
