import lib.crawler as all_crawlers
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
        crawler = all_crawlers.CzbooksCrawler(url)
        website = "czbooks"

    elif url.startswith('https://www.hetubook.com'):
        crawler = all_crawlers.HetubookCrawler(url)
        website = "hetubook"

    elif url.startswith('https://tw.hjwzw.com'):
        crawler = all_crawlers.HjwzwCrawler(url)
        website = "hjwzw"

    elif url.startswith('https://www.novel543.com'):
        crawler = all_crawlers.Novel543Crawler(url)
        website = "novel543"

    elif url.startswith('https://br.supertime01.com'):
        crawler = all_crawlers.Supertime01Crawler(url)
        website = "supertime01"

    elif url.startswith('https://www.timotxt.com'):
        crawler = all_crawlers.TimotxtCrawler(url)
        website = "timotxt"

    elif url.startswith('https://www.ttkan.co'):
        crawler = all_crawlers.TtkanCrawler(url)
        website = "ttkan"

    elif url.startswith('https://tw.uukanshu.net'):
        crawler = all_crawlers.UutwNetCrawler(url)
        website = "uutw_net"

    elif url.startswith('https://tw.zhswx.com'):
        crawler = all_crawlers.ZhswxCrawler(url)
        website = "zhswx"

    else:
        crawler = None
        website = None

    log('[select_crawler]', website, url)

    print(url)

    return crawler, website
