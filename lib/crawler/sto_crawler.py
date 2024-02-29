from lib.crawler.basic_crawler import BasicCrawler
from lib.helper.crawler_helper import make_chapter_file
from lib.helper.requests_helper import get_soup
from lib.utils.logger import log


class StoCrawler(BasicCrawler):
    """Crawler for https://sto520.com

    Args:
        `url`: The url of the book.

    Attributes:
        `base_url`: The prefix of the url.
        `soup`: The soup of the url.
        `title`: The title of the book.
        `author`: The author of the book.
        `chapter_list`: The list of the chapters.
        `chapter_size`: The size of the chapters.
        `path`: The path of the book.

    Functions:
        `set_title`: Get the title of the book.
        `set_author`: Get the author of the book.
        `get_all_pages`: Get the all pages of the book.
        `get_chapter_size`: Get the size of the chapters.
        `get_content`: Get the content of the chapter
            and create the chapter file.
        `translate_title_author`: Translate the title and author of the book.
        `set_path`: Create the directory of the book.
        `get_path`: Get the directory of the book.
        `download`: Download the book.
    """

    def __init__(self, url):

        self.base_url = ""
        self.soup = get_soup(url)

        self.set_title()
        self.set_author()
        self.translate_title_author()

        self.chapter_list = self.get_all_pages()
        self.chapter_size = self.get_chapter_size()
        self.set_path()

        log('[sto_crawler]', self.title, self.author, self.chapter_size)

    def set_title(self):
        """Set the title of the book."""
        self.title = self.soup.find('h1', 'booktitle').text.strip()

    def set_author(self):
        """Set the author of the book."""

        self.author = self.soup.find('a', 'red').text.strip()

    def get_all_pages(self):
        """Get the all pages of the book.

        Returns:
            `chapter_list`: The list of the chapters.
        """

        self.chapter_list = []
        for t in self.soup.find('div', id='list-chapterAll').find_all('a'):
            self.chapter_list.append(self.base_url + t.get('href'))

        return self.chapter_list

    def get_content(self, index):
        """Get the content of the chapter and create the chapter file.

        Args:
            `index`: The index of the chapter.
        """

        soup = get_soup(self.chapter_list[index])

        if soup.find('h1', 'pt10'):
            chapter_name = (
                soup.find('h1', 'pt10')
                .text.replace(self.title, '')
                .replace('《》', '')
            )
        else:
            chapter_name = '第{}章'.format(index)

        if soup.find('p', 'readcotent bbb font-normal'):
            content = soup.find('p', 'readcotent bbb font-normal').text
        else:
            content = '\n\n'

        make_chapter_file(index, chapter_name, content, self.path)
