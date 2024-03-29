from lib.crawler.basic_crawler import BasicCrawler
from lib.helper.crawler_helper import make_chapter_file
from lib.helper.requests_helper import get_soup
from lib.utils.logger import log


class Novel543Crawler(BasicCrawler):
    """Crawler for https://www.novel543.com

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
        `translate_title_author_intro`: Translate the title, author and introduction of the book.
        `set_path`: Create the directory of the book.
        `get_path`: Get the directory of the book.
        `download`: Download the book.
    """

    def __init__(self, url):
        self.base_url = "https://www.novel543.com"
        self.soup = get_soup(url)

        self.title, self.author = self.translate_title_author_intro()
        self.chapter_list = self.get_all_pages()
        self.chapter_size = self.get_chapter_size()
        self.set_path()

        log("[novel543_crawler]", self.title, self.author, self.chapter_size)

    def set_title(self):
        """Get the title of the book.

        Returns:
            `title`: The title of the book.
        """

        self.title = (
            self.soup.find("div", "headline")
            .find("h1")
            .text.strip()
            .replace("》", "")
            .replace("《", "")
        )

        return self.title

    def set_author(self):
        """Get the author of the book.

        Returns:
            `author`: The author of the book.
        """

        self.author = (
            self.soup.find("div", "headline")
            .find("h2")
            .a.text.strip()
            .replace("》", "")
            .replace("《", "")
        )
        return self.author

    def get_all_pages(self):
        """Get the all pages of the book.

        Returns:
            `chapter_list`: The list of the chapters.
        """

        self.chapter_list = []
        for t in (
            self.soup.find("div", "read")
            .find_all("dl")[1]
            .find_all("a", rel="nofollow")
        ):
            self.chapter_list.append(self.base_url + t.get("href"))

        return self.chapter_list

    def get_content(self, index):
        """Get the content of the chapter and create the chapter file.

        Args:
            `index`: The index of the chapter.
        """

        soup = get_soup(self.chapter_list[index])

        if soup.find("div", "chapter-content px-3").find("h1"):
            chapter_name = (
                soup.find("div", "chapter-content px-3")
                .find("h1")
                .text.strip()
            )

        else:
            chapter_name = "第{}章".format(index)

        if soup.find("div", "content"):
            content = ""
            for c in soup.find("div", "content"):
                content += c.text.strip() + "\n\n"

        else:
            content = "\n\n"

        make_chapter_file(index, chapter_name, content, self.path)
