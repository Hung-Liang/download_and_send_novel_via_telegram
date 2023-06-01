from lib.crawler.czbooks_crawler import CzbooksCrawler
from lib.crawler.uutw_crawler import UutwCrawler
from lib.crawler.hetubook_crawler import HetubookCrawler
from lib.crawler.zhsxstw_crawler import ZhsxstwCrawler
from lib.utils.file_path import (
    CZBOOKS_CRAWLER_PATH,
    UUTW_CRAWLER_PATH,
    HETUBOOK_CRAWLER_PATH,
    ZHSXSTW_CRAWLER_PATH,
)


def select_crawler(url):
    """Select the crawler by the url.

    Args:
        `url`: The url of the book.

    Returns:
        `crawler`: The crawler of the book.
        `website`: The website of the book.
        `crawler_path`: The path of the crawler.
    """

    if url.startswith('https://czbooks.net'):
        crawler = CzbooksCrawler(url)
        website = "czbooks"
        crawler_path = CZBOOKS_CRAWLER_PATH

    elif url.startswith('https://tw.uukanshu.com'):
        crawler = UutwCrawler(url)
        website = "uutw"
        crawler_path = UUTW_CRAWLER_PATH

    elif url.startswith('https://www.hetubook.com'):
        crawler = HetubookCrawler(url)
        website = "hetubook"
        crawler_path = HETUBOOK_CRAWLER_PATH

    elif url.startswith('http://tw.zhsxs.com/'):
        crawler = ZhsxstwCrawler(url)
        website = "zhsxstw"
        crawler_path = ZHSXSTW_CRAWLER_PATH

    else:
        return None, None, None

    return crawler, website, crawler_path
