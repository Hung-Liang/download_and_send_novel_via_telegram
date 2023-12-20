import os
import sys

project_path = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_path)

import multiprocessing
from lib.helper.requests_helper import get_soup
from lib.helper.crawler_helper import (
    create_directory,
    make_chapter_file,
    merge_chapter,
)
from lib.utils.file_path import OUTPUT_PATH
from lib.tools.translate import translate_simp_to_trad
from lib.utils.logger import log


class HetubookCrawler:
    """Crawler for https://www.hetubook.com

    Args:
        `url`: The url of the book.

    Attributes:
        `url_prefix`: The prefix of the url.
        `soup`: The soup of the url.
        `title`: The title of the book.
        `author`: The author of the book.
        `chapter_list`: The list of the chapters.
        `chapter_size`: The size of the chapters.
        `path`: The path of the book.

    Functions:
        `get_title`: Get the title of the book.
        `get_author`: Get the author of the book.
        `get_all_pages`: Get the all pages of the book.
        `get_chapter_size`: Get the size of the chapters.
        `get_chapter_list`: Get the list of the chapters.
        `get_content`: Get the content of the chapter
            and create the chapter file.
    """

    def __init__(self, url):

        self.url_prefix = "https://www.hetubook.com"
        self.soup = get_soup(url)

        self.title, self.author = translate_simp_to_trad(
            [self.get_title(), self.get_author()]
        )

        self.chapter_list = self.get_all_pages()
        self.chapter_size = self.get_chapter_size()
        self.path = create_directory(OUTPUT_PATH, self.title)

        log('[hetubook_crawler]', self.title, self.author, self.chapter_size)

    def get_title(self):
        """Get the title of the book.

        Returns:
            `title`: The title of the book.
        """

        self.title = (
            self.soup.find('div', 'book_info finish')
            .find('h2')
            .text.strip()
            .replace('》', '')
            .replace('《', '')
        )

        return self.title

    def get_author(self):
        """Get the author of the book.

        Returns:
            `author`: The author of the book.
        """

        self.author = (
            self.soup.find('div', 'book_info finish')
            .find('div')
            .text.strip()
            .replace('作者：', '')
        )
        return self.author

    def get_all_pages(self):
        """Get the all pages of the book.

        Returns:
            `chapter_list`: The list of the chapters.
        """

        self.chapter_list = []
        for t in self.soup.find('dl', id='dir').find_all('a'):
            self.chapter_list.append(self.url_prefix + t.get('href'))

        return self.chapter_list

    def get_chapter_size(self):
        """Get the size of the chapters.

        Returns:
            `chapter_size`: The size of the chapters.
        """

        return len(self.chapter_list)

    def get_content(self, index):
        """Get the content of the chapter and create the chapter file.

        Args:
            `index`: The index of the chapter.
        """

        soup = get_soup(self.chapter_list[index])

        if soup.find_all('h2'):

            chapter_name = ""

            for t in soup.find_all('h2'):
                chapter_name += t.text.strip() + "\n\n"

        else:
            chapter_name = '第{}章'.format(index)

        if soup.find('div', id='content').find_all('div'):
            content = ""
            for t in soup.find('div', id='content').find_all('div'):
                content += t.text.strip() + "\n\n"

        else:
            content = '\n\n'

        make_chapter_file(index, chapter_name, content, self.path)


if __name__ == '__main__':

    downloader = HetubookCrawler(sys.argv[1])

    pool = multiprocessing.Pool()
    pool.map(
        downloader.get_content,
        range(0, len(downloader.chapter_list)),
    )
    pool.close()

    merge_chapter(downloader.path, downloader.title, downloader.chapter_size)
