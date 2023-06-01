import os
from pathlib import Path


PROGRAM_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

LOG_PATH = Path(PROGRAM_PATH, 'log')
OUTPUT_PATH = Path(PROGRAM_PATH, 'output')
ASSET_PATH = Path(PROGRAM_PATH, 'asset')
CRAWLER_ROOT_PATH = Path(PROGRAM_PATH, 'lib', 'crawler')

CZBOOKS_CRAWLER_PATH = Path(CRAWLER_ROOT_PATH, 'czbooks_crawler.py')
UUTW_CRAWLER_PATH = Path(CRAWLER_ROOT_PATH, 'uutw_crawler.py')
HETUBOOK_CRAWLER_PATH = Path(CRAWLER_ROOT_PATH, 'hetubook_crawler.py')
ZHSXSTW_CRAWLER_PATH = Path(CRAWLER_ROOT_PATH, 'zhsxstw_crawler.py')
STO_CRAWLER_PATH = Path(CRAWLER_ROOT_PATH, 'sto_crawler.py')

BOOKS_JSON_PATH = Path(ASSET_PATH, 'books.json')

LOG_PATH.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
ASSET_PATH.mkdir(parents=True, exist_ok=True)
