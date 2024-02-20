from lib.crawler.basic_crawler import BasicCrawler
from lib.helper.crawler_helper import make_chapter_file
from lib.helper.requests_helper import get_soup
from lib.utils.logger import log


class ZhsxstwCrawler(BasicCrawler):
    """Crawler for http://tw.zhsshu.com/

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

        if "book" in url:
            url = url.replace("zhsbook", "zhschapter")

        self.base_url = "http://tw.zhsxs.com"
        self.soup = get_soup(url)

        self.title, self.author = self.translate_title_author()

        self.chapter_list = self.get_all_pages()
        self.chapter_size = self.get_chapter_size()

        self.set_path()

        log('[zhsxstw_crawler]', self.title, self.author, self.chapter_size)

    def set_title(self):
        """Get the title of the book.

        Returns:
            `title`: The title of the book.
        """

        self.title = (
            self.soup.find('td')
            .find_all('a')[1]
            .get('title')
            .split(' ')[0]
            .replace('《', '')
            .replace('》', '')
        )

        return self.title

    def set_author(self):
        """Get the author of the book.

        Returns:
            `author`: The author of the book.
        """

        self.author = (
            self.soup.find('td')
            .find_all('a')[1]
            .get('title')
            .split(' ')[1]
            .replace('《', '')
            .replace('》', '')
        )

        return self.author

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
