from lib.crawler import (
    CzbooksCrawler,
    HetubookCrawler,
    HjwzwCrawler,
    Novel543Crawler,
    Supertime01Crawler,
    TtkanCrawler,
    UutwNetCrawler,
    ZhswxCrawler,
)
from lib.utils.logger import log


def select_crawler(url: str):
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

    elif url.startswith('https://www.hetubook.com'):
        crawler = HetubookCrawler(url)
        website = "hetubook"

    elif url.startswith('https://tw.hjwzw.com'):
        crawler = HjwzwCrawler(url)
        website = "hjwzw"

    elif url.startswith('https://www.novel543.com'):
        crawler = Novel543Crawler(url)
        website = "novel543"

    elif url.startswith('https://br.supertime01.com'):
        crawler = Supertime01Crawler(url)
        website = "supertime01"

    elif url.startswith('https://www.ttkan.co'):
        crawler = TtkanCrawler(url)
        website = "ttkan"

    elif url.startswith('https://tw.uukanshu.net'):
        crawler = UutwNetCrawler(url)
        website = "uutw_net"

    elif url.startswith('https://tw.zhswx.com'):
        crawler = ZhswxCrawler(url)
        website = "zhswx"

    else:
        crawler = None
        website = None

    log('[select_crawler]', website, url)

    return crawler, website
