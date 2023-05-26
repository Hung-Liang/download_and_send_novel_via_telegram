import requests
from bs4 import BeautifulSoup
from lib.utils.logger import log


def fetch(url: str, counter=0):

    if counter > 5:
        raise Exception('Fetch failed')

    headers = {
        'User-Agent': (
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML,"
            " like Gecko) Chrome/39.0.2171.95 Safari/537.36"
        )
    }

    res = requests.get(url, headers=headers)

    log('[requests_helper]', f'fetch: {res.status_code} {url}')

    if res.status_code != 200:
        fetch(url, counter + 1)
    else:
        return res.text


def get_soup(url=None, response_text=None):
    if response_text:
        return BeautifulSoup(response_text, 'lxml')
    elif url:
        return BeautifulSoup(fetch(url), 'lxml')
    else:
        raise Exception('get_soup: url or response_text must be provided')


def find_element(soup, class_tag, class_name):
    return soup.find(class_tag, class_name)
