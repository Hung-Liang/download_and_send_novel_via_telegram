import os
from pathlib import Path


PROGRAM_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

LOG_PATH = Path(PROGRAM_PATH, 'log')
OUTPUT_PATH = Path(PROGRAM_PATH, 'output')
ASSET_PATH = Path(PROGRAM_PATH, 'asset')
CRAWLER_ROOT_PATH = Path(PROGRAM_PATH, 'lib', 'crawler')
TEMP_PATH = Path(PROGRAM_PATH, 'temp')

CRAWLER_HANDLER_PATH = Path(PROGRAM_PATH, 'lib', 'tools', 'crawler_handler.py')

BOOKS_JSON_PATH = Path(ASSET_PATH, 'books.json')

LOG_PATH.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
ASSET_PATH.mkdir(parents=True, exist_ok=True)
