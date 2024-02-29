import re

from lib.crawler.basic_crawler import BasicCrawler
from lib.helper.crawler_helper import make_chapter_file
from lib.helper.requests_helper import get_soup
from lib.utils.logger import log


class ZhswxCrawler(BasicCrawler):
    """Crawler for http://tw.zhswx.com/

    Args:
        `url`: The url of the book.

    Attributes:
        `url`: The url of the book.
        `base_url`: The prefix of the url.
        `soup`: The soup of the url.
        `title`: The title of the book.
        `author`: The author of the book.
        `intro`: The introduction of the book.
        `chapter_list`: The list of the chapters.
        `chapter_size`: The size of the chapters.
        `path`: The path of the book.

    Functions:
        `setup`: Set up the basic information of the book.
        `set_title`: Get the title of the book.
        `set_author`: Get the author of the book.
        `set_intro`: Get the introduction of the book.
        `get_title`: Get the title of the book.
        `get_author`: Get the author of the book.
        `get_intro`: Get the introduction of the book.
        `get_all_pages`: Get the all pages of the book.
        `get_chapter_size`: Get the size of the chapters.
        `get_content`: Get the content of the chapter
            and create the chapter file.
        `translate_title_author_intro`:
            Translate the title, author and introduction of the book.
        `set_path`: Create the directory of the book.
        `get_path`: Get the directory of the book.
        `download`: Download the book.
    """

    def __init__(self, url):
        super().__init__(url)

        if "book" in self.url:
            self.url = self.url.replace("book", "chapter")

        self.info_url = self.url.replace("chapter", "book")

        self.base_url = "https://tw.zhswx.com"
        self.soup = get_soup(url)

        self.setup()

        log('[zhsxstw_crawler]', self.title, self.author, self.chapter_size)

    def set_title(self):
        """Set the title of the book."""
        soup = get_soup(self.info_url)

        self.title = soup.find('div', id='novel_title').text.strip()

    def set_author(self):
        """Set the author of the book."""
        soup = get_soup(self.info_url)

        self.author = soup.find('a', title=re.compile(r"^作者標簽:")).text.strip()

    def set_intro(self):
        """Set the introduction of the book."""
        soup = get_soup(self.info_url)

        self.intro = (
            soup.find('div', style="line-height: 30px")
            .text.split("【內容簡介】")[1]
            .replace("開始閱讀", "")
            .replace("開始閱讀", "")
            .strip()
        )

    def get_all_pages(self):
        """Get the all pages of the book.

        Returns:
            `chapter_list`: The list of the chapters.
        """

        self.chapter_list = []

        for t in self.soup.find_all('td', 'chapterlist'):
            if t.a.get('href'):
                self.chapter_list.append(self.base_url + t.a.get('href'))

        return self.chapter_list

    def get_content(self, index):
        """Get the content of the chapter and create the chapter file.

        Args:
            `index`: The index of the chapter.
        """

        soup = get_soup(self.chapter_list[index])

        if soup.find_all('td')[1].find('h1').text:
            chapter_name = (
                soup.find_all('td')[1]
                .find('h1')
                .text.replace(self.title, '')
                .replace('《》', '')
                .strip()
            )
        else:
            chapter_name = '第{}章'.format(index)

        if soup.find_all('td')[1].find_all('div')[8].text:
            content = soup.find_all('td')[1].find_all('div')[8].text
        else:
            content = '\n\n'

        make_chapter_file(index, chapter_name, content, self.path)
