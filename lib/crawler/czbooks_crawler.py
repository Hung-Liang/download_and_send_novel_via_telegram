from lib.helper.requests_helper import get_soup, find_element


class CZBookPreCrawler:
    def __init__(self, url):
        self.soup = get_soup(url)

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
            self.chapter_list.append(t.get('href'))

        return self.chapter_list

    def get_chapter_number(self):
        return len(self.chapter_list)


class CZBookCrawler(CZBookPreCrawler):
    def get_content():
        pass
