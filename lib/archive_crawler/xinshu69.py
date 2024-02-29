from lib.crawler.basic_crawler import BasicCrawler
from lib.helper.crawler_helper import make_chapter_file
from lib.helper.requests_helper import get_soup, fetch
from lib.utils.logger import log


class XinShu69(BasicCrawler):
    """Crawler for https://www.69xinshu.com/

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
        res_text = bytes(fetch(url), 'latin1').decode('gb2312')
        self.soup = get_soup(response_text=res_text)

        self.chapter_list = self.get_all_pages()

        self.set_title()
        self.set_author()
        self.set_intro()
        self.translate_title_author_intro()

        self.chapter_size = self.get_chapter_size()

        self.set_path()

        log('[czbooks_crawler]', self.title, self.author, self.chapter_size)

    def set_title(self):
        """Set the title of the book."""

        self.title = (
            self.soup.find('div', 'bread')
            .find_all('a')[-2]
            .text.strip()
            .replace('》', '')
            .replace('《', '')
        )

    def set_author(self):
        """Set the author of the book."""

        res_text = bytes(fetch(self.chapter_list[0]), 'latin1').decode(
            'gb2312', 'replace'
        )

        soup = get_soup(response_text=res_text)

        self.author = (
            (
                soup.find('div', 'txtinfo hide720')
                .find_all('span')[-1]
                .text.strip()
            )
            .replace('作者：', '')
            .strip()
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
        for t in self.soup.find('div', id='catalog').find_all('a'):
            self.chapter_list.append(self.base_url + t.get('href'))

        return self.chapter_list

    def get_content(self, index):
        """Get the content of the chapter and create the chapter file.

        Args:
            `index`: The index of the chapter.
        """

        res_text = bytes(fetch(self.chapter_list[index]), 'latin1').decode(
            'gb2312', 'replace'
        )
        soup = get_soup(response_text=res_text)

        if soup.find('h1', 'hide720'):
            chapter_name = (
                soup.find('h1', 'hide720')
                .text.replace(self.title, '')
                .replace('《》', '')
            )
        else:
            chapter_name = '第{}章'.format(index)

        if soup.find('div', 'txtnav'):
            content = "\n".join(
                soup.find('div', 'txtnav').text.splitlines()[3:]
            )
        else:
            content = '\n\n'

        make_chapter_file(index, chapter_name, content, self.path)
