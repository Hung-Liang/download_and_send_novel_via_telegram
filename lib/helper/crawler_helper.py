from pathlib import Path
import re
from lib.tools.tools import delete_file
from lib.tools.translate import translate_simp_to_trad


def create_directory(path, title):
    """Create a directory for the novel.

    Args:
        `path`: The path to create the directory.
        `title`: The title of the novel.

    Returns:
        The path of the directory.
    """

    path = Path(path, title)
    path.mkdir(parents=True, exist_ok=True)
    return path


def is_chapter_line(line):
    """Check if the line is a chapter line.

    Args:
        `line`: A line of text.

    Returns:
        True if the line is a chapter line, False otherwise.
    """

    pattern = (
        r"(\s+|\n|)(第)([\u4e00-\u9fa5a-zA-Z0-9]{1,7})"
        r"[章節卷集部篇回][^\n]{1,35}(|\n)"
    )
    result = re.match(pattern, line)

    if result:
        return True
    else:
        return False


def make_chapter_file(index, chapter_name, content, novel_path):
    """Make a chapter's file in given path.

    Args:
        `index`: The index of the chapter.
        `chapter_name`: The name of the chapter.
        `content`: The content of the chapter.
        `novel_path`: The path of the novel.
    """

    chapter_path = Path(novel_path, str(index))

    with open(chapter_path, 'w', encoding='utf-8') as f:

        f.write('# ' + chapter_name + '\n\n\n\n')

        lines = content.splitlines()

        for line in lines:  # 排版
            if line != '':
                if line == is_chapter_line(line):
                    f.write('# ' + line.strip() + '\n\n')
                else:
                    f.write('       ' + line.strip() + '\n\n')


def delete_chapter(path, chapter_size):
    """Delete the chapter files.

    Args:
        `path`: The path of the novel.
        `chapter_size`: The size of the chapter.
    """

    for i in range(chapter_size):
        chapter_path = Path(path, str(i))
        delete_file(chapter_path)


def merge_chapter(path, title, author, intro, chapter_size):
    """Merge the chapter files.

    Args:
        `path`: The path of the novel.
        `title`: The title of the novel.
        `intro`: The introduction of the novel.
        `chapter_size`: The size of the chapter.
    """

    with open(Path(path, "{}.txt".format(title)), 'w', encoding='utf-8') as f:
        f.write('書名: ' + title + '\n')
        f.write('作者: ' + author + '\n\n')
        f.write("介紹:\n")
        for line in intro.splitlines():
            f.write('       ' + line.strip() + '\n')
        f.write('\n\n')

    for i in range(chapter_size):
        with open(Path(path, str(i)), 'r', encoding='utf-8') as f:
            lines = f.readlines()

        lines = translate_simp_to_trad(lines)

        with open(
            Path(path, "{}.txt".format(title)), 'a', encoding='utf-8'
        ) as f:
            f.writelines(lines)

    delete_chapter(path, chapter_size)
