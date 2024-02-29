from lib.crawler.basic_crawler import BasicCrawler
from lib.helper.crawler_helper import make_chapter_file
from lib.helper.requests_helper import get_soup, fetch
from lib.utils.logger import log
import json


class TtkanCrawler(BasicCrawler):
    """Crawler for https://www.ttkan.co

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

        self.base_url = "https://www.ttkan.co"
        self.chapter_url = "https://www.bg3.co/novel/pagea/{}".format(
            url.split('/')[-1]
        )

        self.soup = get_soup(url)

        self.setup()

        log('[sto_crawler]', self.title, self.author, self.chapter_size)

    def set_title(self):
        """Set the title of the book."""

        self.title = (
            self.soup.find(
                'div', 'pure-u-xl-5-6 pure-u-lg-5-6 pure-u-md-2-3 pure-u-1-2'
            )
            .find_all("li")[0]
            .text.strip()
        )

    def set_author(self):
        """Set the author of the book."""

        self.author = (
            self.soup.find(
                'div', 'pure-u-xl-5-6 pure-u-lg-5-6 pure-u-md-2-3 pure-u-1-2'
            )
            .find_all("li")[1]
            .text.strip()
            .replace('作者：', '')
        )

    def set_intro(self):
        """Set the introduction of the book."""

        self.intro = self.soup.find('div', 'description').text.strip()

    def get_all_pages(self):
        """Get the all pages of the book.

        Returns:
            `chapter_list`: The list of the chapters.
        """

        url = (
            self.base_url
            + self.soup.find('button', id='button_show_all_chatper')[
                'on'
            ].split("'")[1]
        )

        self.chapter_list = json.loads(fetch(url))["items"]

        return self.chapter_list

    def get_content(self, index):
        """Get the content of the chapter and create the chapter file.

        Args:
            `index`: The index of the chapter.
        """

        chapter_id = self.chapter_list[index]["chapter_id"]
        chapter_name = self.chapter_list[index]["chapter_name"]

        full_chapter_url = self.chapter_url + "_{}.html".format(chapter_id)

        soup = get_soup(full_chapter_url)

        if soup.find('div', 'content'):
            content = soup.find('div', 'content').text.replace(
                "章節報錯 分享給朋友：", ""
            )
            # content = "\n\n".join(content.splitlines()[:-1])
        else:
            content = '\n\n'

        make_chapter_file(index, chapter_name, content, self.path)
