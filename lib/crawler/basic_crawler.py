import concurrent.futures

from lib.helper.crawler_helper import create_directory, merge_chapter
from lib.tools.translate import translate_simp_to_trad
from lib.utils.file_path import OUTPUT_PATH


class BasicCrawler:
    """Basic crawler for the crawler.

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

        self.url = url

        self.base_url = None
        self.soup = None

        self.title, self.author, self.intro = None, None, None

        self.chapter_list = None
        self.chapter_size = None
        self.path = None

    def setup(self):
        """Set up the basic information of the book."""
        self.set_title()
        self.set_author()
        self.set_intro()
        self.translate_title_author_intro()

        self.chapter_list = self.get_all_pages()
        self.chapter_size = self.get_chapter_size()
        self.set_path()

    def set_title(self):
        """Set the title of the book."""
        pass

    def set_author(self):
        """Set the author of the book."""
        pass

    def set_intro(self):
        """Set the introduction of the book."""
        pass

    def get_title(self):
        """Get the title of the book."""
        return self.title

    def get_author(self):
        """Get the author of the book."""
        return self.author

    def get_intro(self):
        """Get the introduction of the book."""
        return self.intro

    def get_all_pages(self):
        """Get the all pages of the book."""
        pass

    def get_chapter_size(self):
        """Get the size of the chapters.

        Returns:
            `chapter_size`: The size of the chapters.
        """
        return len(self.chapter_list)

    def get_content(self):
        """Get the content of the chapter"""
        pass

    def translate_title_author_intro(self):
        """Translate the title, author and introduction of the book."""

        if self.title:
            self.title = translate_simp_to_trad([self.title])[0]

        if self.author:
            self.author = translate_simp_to_trad([self.author])[0]

        if self.intro:
            self.intro = translate_simp_to_trad([self.intro])[0]

    def set_path(self):
        """Create the directory of the book."""
        self.path = create_directory(OUTPUT_PATH, self.title)

    def get_path(self):
        """Get the directory of the book."""
        return self.path

    def download(self):
        """Download the book."""

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.get_content, range(0, len(self.chapter_list)))

        merge_chapter(
            self.path, self.title, self.author, self.intro, self.chapter_size
        )
