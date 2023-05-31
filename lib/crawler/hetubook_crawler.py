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
from lib.tools.translate import translate_simp_to_trad


class HetubookCrawler:
    def __init__(self, url):

        self.url_prefix = "https://www.hetubook.com"
        self.soup = get_soup(url)

        self.title, self.author = translate_simp_to_trad(
            [self.get_title(), self.get_author()]
        )

        self.chapter_list = self.get_total_pages()
        self.chapter_size = self.get_chapter_size()
        self.path = create_directory(OUTPUT_PATH, self.title)

    def get_title(self):

        self.title = (
            find_element(self.soup, 'div', 'book_info finish')
            .find('h2')
            .text.strip()
            .replace('》', '')
            .replace('《', '')
        )

        return self.title

    def get_author(self):
        self.author = (
            find_element(self.soup, 'div', 'book_info finish')
            .find('div')
            .text.strip()
            .replace('作者：', '')
        )
        return self.author

    def get_total_pages(self):

        self.chapter_list = []
        for t in self.soup.find('dl', id='dir').find_all('a'):
            self.chapter_list.append(self.url_prefix + t.get('href'))

        return self.chapter_list

    def get_chapter_size(self):
        return len(self.chapter_list)

    def get_content(self, index):

        soup = get_soup(self.chapter_list[index])

        if soup.find_all('h2'):

            chapter_name = ""

            for t in soup.find_all('h2'):
                chapter_name += t.text.strip() + "\n\n"

        else:
            chapter_name = '第{}章'.format(index)

        if soup.find('div', id='content').find_all('div'):
            content = ""
            for t in soup.find('div', id='content').find_all('div'):
                content += t.text.strip() + "\n\n"

        else:
            content = '\n\n'

        make_chapter_file(index, chapter_name, content, self.path)


if __name__ == '__main__':

    downloader = HetubookCrawler(sys.argv[1])

    chapter_list = downloader.chapter_list

    pool = multiprocessing.Pool()
    pool.map(
        downloader.get_content,
        range(0, len(chapter_list)),
    )
    pool.close()

    merge_chapter(downloader.path, downloader.title, downloader.chapter_size)
