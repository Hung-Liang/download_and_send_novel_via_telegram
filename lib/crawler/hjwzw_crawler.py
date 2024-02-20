from lib.crawler.basic_crawler import BasicCrawler
from lib.helper.crawler_helper import make_chapter_file
from lib.helper.requests_helper import get_soup
from lib.utils.logger import log
import re


class HjwzwCrawler(BasicCrawler):
    """Crawler for https://tw.hjwzw.com/

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

        self.url_prefix = "https://tw.hjwzw.com"
        self.soup = get_soup(url)

        self.title, self.author = self.translate_title_author()

        self.chapter_list = self.get_all_pages()
        self.chapter_size = self.get_chapter_size()
        self.set_path()

        log('[hiwzw_crawler]', self.title, self.author, self.chapter_size)

    def set_title(self):
        """Get the title of the book.

        Returns:
            `title`: The title of the book.
        """

        self.title = (
            self.soup.find('h1').text.strip().replace('》', '').replace('《', '')
        )

        return self.title

    def set_author(self):
        """Get the author of the book.

        Returns:
            `author`: The author of the book.
        """

        self.author = self.soup.find(
            'a', title=re.compile(r"^作者:")
        ).text.strip()
        return self.author

    def get_all_pages(self):
        """Get the all pages of the book.

        Returns:
            `chapter_list`: The list of the chapters.
        """

        self.chapter_list = []
        for t in self.soup.find('div', id='tbchapterlist').find_all('td'):
            if t.a:
                self.chapter_list.append(self.url_prefix + t.a.get('href'))

        return self.chapter_list

    def get_content(self, index):
        """Get the content of the chapter and create the chapter file.

        Args:
            `index`: The index of the chapter.
        """

        soup = get_soup(self.chapter_list[index])

        if soup.find('h1'):
            chapter_name = soup.find('h1').text.strip() + "\n\n"

        else:
            chapter_name = '第{}章'.format(index)

        content_div = soup.find(
            lambda tag: tag.name == 'div'
            and tag.get('style')
            == 'font-size: 20px; line-height: 30px; word-wrap: break-word;'
            ' table-layout: fixed; word-break: break-all; width: 750px;'
            ' margin: 0 auto; text-indent: 2em;'
        )

        content = ""
        if content_div:
            content = content_div.text.strip() + "\n\n"

        else:
            content = "\n\n"

        content = "\n\n".join(content.splitlines()[2:])

        make_chapter_file(index, chapter_name, content, self.path)