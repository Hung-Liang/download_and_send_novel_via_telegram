from lib.crawler.basic_crawler import BasicCrawler
from lib.helper.crawler_helper import make_chapter_file
from lib.helper.requests_helper import get_soup
from lib.utils.logger import log


class Supertime01Crawler(BasicCrawler):
    """Crawler for https://br.supertime01.com/

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

        self.base_url = ""
        self.soup = get_soup(url)

        self.setup()

        log('[czbooks_crawler]', self.title, self.author, self.chapter_size)

    def set_title(self):
        """Set the title of the book."""

        self.title = (
            self.soup.find('b', 'name')
            .text.strip()
            .replace('》', '')
            .replace('《', '')
        )

    def set_author(self):
        """Set the author of the book."""

        self.author = (
            self.soup.find('div', 'author').text.strip().replace('作者 :', '')
        )

    def set_intro(self):
        """Set the introduction of the book."""

        self.intro = ""

    def get_all_pages(self):
        """Get the all pages of the book.

        Returns:
            `chapter_list`: The list of the chapters.
        """

        self.chapter_list = []
        for t in self.soup.find('ul', 'chapterlist').find_all('a'):
            self.chapter_list.append(self.base_url + t.get('href'))

        return self.chapter_list

    def get_content(self, index):
        """Get the content of the chapter and create the chapter file.

        Args:
            `index`: The index of the chapter.
        """

        soup = get_soup(self.chapter_list[index])

        chapter_name = '第{}章'.format(index)

        if soup.find('div', 'novelcontent'):
            lines = soup.find('div', 'novelcontent').find_all('p')
            content = '\n\n'.join([line.text for line in lines])

        else:
            content = '\n\n'

        make_chapter_file(index, chapter_name, content, self.path)
