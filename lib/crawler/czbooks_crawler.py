from lib.helper.requests_helper import get_soup, find_element
from pathlib import Path
from lib.utils.file_path import OUTPUT_PATH
from lib.tools.tools import create_directory


class CZBookPreCrawler:
    def __init__(self, url):

        self.soup = get_soup(url)
        self.title = self.get_title()
        self.author = self.get_author()
        self.chapter_list = self.get_total_pages()

    def get_title(self):

        self.title = (
            find_element(self.soup, 'span', 'title')
            .text.strip()
            .replace('》', '')
            .replace('《', '')
        )

        return self.title

    def get_author(self):
        self.author = find_element(self.soup, 'span', 'author').a.text.strip()
        return self.author

    def get_total_pages(self):

        self.chapter_list = []
        for t in find_element(self.soup, 'ul', 'nav chapter-list').find_all(
            'a'
        ):
            self.chapter_list.append("https:" + t.get('href'))

        return self.chapter_list

    def get_chapter_number(self):
        return len(self.chapter_list)


class CZBookCrawler(CZBookPreCrawler):
    def __init__(self, url):

        super().__init__(url)
        self.path = create_directory(OUTPUT_PATH, self.title)

    def get_content(self):

        pass
        # soup = get_soup("https:" + url)

        # if find_element(soup, 'div', 'name'):
        #     chapter_name = (
        #         find_element(soup, 'div', 'name')
        #         .text.replace(self.title, '')
        #         .replace('《》', '')
        #     )
        # else:
        #     chapter_name = '第{}章'.format(index)

        # if find_element(soup, 'div', 'content'):
        #     content = find_element(soup, 'div', 'content').text
        # else:
        #     content = '\n\n'

        # (index, chapter_name, content)
