from pathlib import Path


def create_directory(path, title):

    path = Path(path, title)
    path.mkdir(parents=True, exist_ok=True)
    return path


def merge_chapter(path, title, chapter_size):

    pass
