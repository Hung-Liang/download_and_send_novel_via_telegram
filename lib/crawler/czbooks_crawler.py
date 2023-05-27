import os
import sys

project_path = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_path)

import multiprocessing
from lib.helper.requests_helper import find_element, get_soup
from lib.tools.crawler_helper import (
    create_directory,
    make_chapter_file,
    merge_chapter,
)
from lib.utils.file_path import OUTPUT_PATH


class CzbooksCrawler:
    def __init__(self, url):

        self.soup = get_soup(url)
        self.title = self.get_title()
        self.author = self.get_author()
        self.chapter_list = self.get_total_pages()
        self.chapter_size = self.get_chapter_size()
        self.path = create_directory(OUTPUT_PATH, self.title)

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

    def get_chapter_size(self):
        return len(self.chapter_list)

    def get_content(self, index):

        soup = get_soup(self.chapter_list[index])

        if find_element(soup, 'div', 'name'):
            chapter_name = (
                find_element(soup, 'div', 'name')
                .text.replace(self.title, '')
                .replace('《》', '')
            )
        else:
            chapter_name = '第{}章'.format(index)

        if find_element(soup, 'div', 'content'):
            content = find_element(soup, 'div', 'content').text
        else:
            content = '\n\n'

        make_chapter_file(index, chapter_name, content, self.path)


if __name__ == '__main__':

    downloader = CzbooksCrawler(sys.argv[1])

    chapter_list = downloader.chapter_list

    downloader.get_content(0)

    pool = multiprocessing.Pool()
    pool.map(
        downloader.get_content,
        range(0, len(chapter_list)),
    )
    pool.close()

    merge_chapter(downloader.path, downloader.title, downloader.chapter_size)
