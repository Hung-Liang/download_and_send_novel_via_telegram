import os
from pathlib import Path


PROGRAM_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

LOG_PATH = Path(PROGRAM_PATH, 'log')
OUTPUT_PATH = Path(PROGRAM_PATH, 'output')
ASSET_PATH = Path(PROGRAM_PATH, 'asset')

LOG_PATH.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
ASSET_PATH.mkdir(parents=True, exist_ok=True)
