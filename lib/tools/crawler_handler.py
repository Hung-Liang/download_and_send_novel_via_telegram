from lib.crawler.czbooks_crawler import CzbooksCrawler
from lib.crawler.uutw_crawler import UutwCrawler
from lib.utils.file_path import CZBOOKS_CRAWLER_PATH, UUTW_CRAWLER_PATH


def select_crawler(url):

    if url.startswith('https://czbooks.net'):
        crawler = CzbooksCrawler(url)
        website = "czbooks"
        crawler_path = CZBOOKS_CRAWLER_PATH

    elif url.startswith('https://tw.uukanshu.com'):
        crawler = UutwCrawler(url)
        website = "uutw"
        crawler_path = UUTW_CRAWLER_PATH

    else:

        return None, None, None

    return crawler, website, crawler_path
