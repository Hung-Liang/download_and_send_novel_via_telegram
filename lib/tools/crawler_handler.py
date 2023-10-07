from lib.crawler.czbooks_crawler import CzbooksCrawler
from lib.crawler.uutw_crawler import UutwCrawler
from lib.crawler.hetubook_crawler import HetubookCrawler
from lib.crawler.zhsxstw_crawler import ZhsxstwCrawler
from lib.crawler.sto_crawler import StoCrawler
from lib.crawler.novel543_crawler import Novel543Crawler
from lib.crawler.supertime01_crawler import Supertime01Crawler
from lib.crawler.zhsshu_crawler import ZhsshuCrawler

from lib.utils.file_path import (
    CZBOOKS_CRAWLER_PATH,
    UUTW_CRAWLER_PATH,
    HETUBOOK_CRAWLER_PATH,
    ZHSXSTW_CRAWLER_PATH,
    STO_CRAWLER_PATH,
    NOVEL543_CRAWLER_PATH,
    SUPERTIME01_CRAWLER_PATH,
    ZHSSHU_CRAWLER_PATH,
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

    elif url.startswith('http://tw.zhsxs.com'):
        crawler = ZhsxstwCrawler(url)
        website = "zhsxstw"
        crawler_path = ZHSXSTW_CRAWLER_PATH

    elif url.startswith('https://tw.zhsshu.com'):
        crawler = ZhsshuCrawler(url)
        website = "zhsshu"
        crawler_path = ZHSSHU_CRAWLER_PATH

    elif url.startswith('https://sto520.com'):
        crawler = StoCrawler(url)
        website = "sto"
        crawler_path = STO_CRAWLER_PATH

    elif url.startswith('https://www.novel543.com'):
        crawler = Novel543Crawler(url)
        website = "novel543"
        crawler_path = NOVEL543_CRAWLER_PATH

    elif url.startswith('https://br.supertime01.com/'):
        crawler = Supertime01Crawler(url)
        website = "supertime01"
        crawler_path = SUPERTIME01_CRAWLER_PATH

    else:
        return None, None, None

    return crawler, website, crawler_path
