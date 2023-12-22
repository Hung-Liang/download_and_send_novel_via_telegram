from lib.crawler.czbooks_crawler import CzbooksCrawler
from lib.crawler.hetubook_crawler import HetubookCrawler
from lib.crawler.novel543_crawler import Novel543Crawler
from lib.crawler.sto_crawler import StoCrawler
from lib.crawler.supertime01_crawler import Supertime01Crawler
from lib.crawler.uutw_crawler import UutwCrawler
from lib.crawler.zhsshu_crawler import ZhsshuCrawler
from lib.crawler.zhsxstw_crawler import ZhsxstwCrawler


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

    elif url.startswith('https://tw.uukanshu.com'):
        crawler = UutwCrawler(url)
        website = "uutw"

    elif url.startswith('https://www.hetubook.com'):
        crawler = HetubookCrawler(url)
        website = "hetubook"

    elif url.startswith('http://tw.zhsxs.com'):
        crawler = ZhsxstwCrawler(url)
        website = "zhsxstw"

    elif url.startswith('https://tw.zhsshu.com'):
        crawler = ZhsshuCrawler(url)
        website = "zhsshu"

    elif url.startswith('https://sto520.com'):
        crawler = StoCrawler(url)
        website = "sto"

    elif url.startswith('https://www.novel543.com'):
        crawler = Novel543Crawler(url)
        website = "novel543"

    elif url.startswith('https://br.supertime01.com/'):
        crawler = Supertime01Crawler(url)
        website = "supertime01"

    else:
        return None, None

    return crawler, website
