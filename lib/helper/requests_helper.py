import requests


def fetch(url, counter=0):
    if counter > 5:
        raise Exception('Fetch ')
    headers = {
        'User-Agent': (
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML,"
            " like Gecko) Chrome/39.0.2171.95 Safari/537.36"
        )
    }
    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        fetch(url, counter + 1)

    return res.text
