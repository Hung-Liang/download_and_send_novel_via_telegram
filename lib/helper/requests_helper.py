import requests
from bs4 import BeautifulSoup
from lib.utils.logger import log


def fetch(url: str, counter=0):
    """Fetch url with requests, if failed, retry 5 times

    Args:
        `url`: url to fetch
        `counter`: counter for retry

    Returns:
        `res.text`: response text
    """

    if counter > 5:
        raise Exception('Fetch failed')

    headers = {
        'User-Agent': (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
            " Edg/117.0.2045.41"
        )
    }

    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        log('[requests_helper]', f'fetch: {res.status_code} {url} {res.text}')
        fetch(url, counter + 1)
    else:
        return res.text


def get_soup(url=None, response_text=None):
    """Get soup from url or response text

    Args:
        `url`: url to fetch
        `response_text`: response text

    Returns:
        `BeautifulSoup`: soup
    """

    if response_text:
        return BeautifulSoup(response_text, 'lxml')
    elif url:
        return BeautifulSoup(fetch(url), 'lxml')
    else:
        raise Exception('get_soup: url or response_text must be provided')
