from lib.tools.tools import load_json, save_json
from lib.utils.file_path import BOOKS_JSON_PATH


def check_book(title, website, length):
    """check book in books.json

    Args:
        `title`: book title
        `website`: website name
        `length`: chapter length

    Returns:
        True, True, True: book exist, website exist, length match
        True, True, False: book exist, website exist, length not match
        True, False, False: book exist, website not exist, length not match
        False, False, False: book not exist,
            website not exist, length not match
    """
    books = load_json(BOOKS_JSON_PATH)

    for book in books:
        if book == title:

            if website in books[book]['websites']:
                if int(books[book]['websites'][website]['length']) == length:

                    fid = books[book]['websites'][website]['fid']
                    return True, True, True, fid
                else:
                    return True, True, False, None
            else:
                return True, False, False, None

    return False, False, False, None


def get_websites(title):
    """Find websites of one book in books.json

    Args:
        `title`: book title

    Returns:
        book exist, websites
    """
    books = load_json(BOOKS_JSON_PATH)

    for book in books:
        if book == title:
            return True, books[book]['websites']

    return False, None


def get_url(title, website):
    """Find url of one website in books.json

    Args:
        `title`: book title
        `website`: website name

    Returns:
        book's url
    """
    books = load_json(BOOKS_JSON_PATH)

    return books[title]['websites'][website]['url']


def get_fid(title, website):
    """Find fid of one website in books.json

    Args:
        `title`: book title
        `website`: website name

    Returns:
        book's fid
    """
    books = load_json(BOOKS_JSON_PATH)

    return books[title]['websites'][website]['fid']


def get_all_fid():
    """Find all fid in books.json

    Args:
        `title`: book title
        `website`: website name

    Returns:
        all fid
    """
    books = load_json(BOOKS_JSON_PATH)
    fid_list = []
    for book in books:
        for website in books[book]['websites']:
            fid_list.append(books[book]['websites'][website]['fid'])

    return fid_list


def add_book(title, author):
    """Add book to books.json

    Args:
        `title`: book title
        `author`: book author
    """
    books = load_json(BOOKS_JSON_PATH)

    book = {
        "author": author,
        "websites": {},
    }

    books[title] = book

    save_json(BOOKS_JSON_PATH, books)


def add_website(title, website, url, fid, length):
    """Add website to books.json

    Args:
        `title`: book title
        `website`: website name
        `url`: website url
        `fid`: file id
        `length`: chapter length
    """
    books = load_json(BOOKS_JSON_PATH)

    book = {
        "url": url,
        "fid": fid,
        "length": length,
    }

    books[title]['websites'][website] = book

    save_json(BOOKS_JSON_PATH, books)


def get_all_books_info():
    """Get all books info from books.json

    Returns:
        all books info
    """
    books = load_json(BOOKS_JSON_PATH)

    info = ""

    for book in books:
        info += "{}  作者: {}\n".format(book, books[book]['author'])

    return info


def delete_website(title, website):
    """Delete website from books.json

    Args:
        `title`: book title
        `website`: website name
    """
    books = load_json(BOOKS_JSON_PATH)

    del books[title]['websites'][website]

    save_json(BOOKS_JSON_PATH, books)
