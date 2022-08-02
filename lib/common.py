import json
import os
from lib.telegramLibrary import telegramLibrary
from lib.czbookFetcher import czbookFetcher
import subprocess
from time import sleep

def getEverythingReady():
    if not os.path.exists('src'):
        os.mkdir('src')
    if not os.path.exists('temp'):
        os.mkdir('temp')
    if not os.path.exists('src/sent.json'):
        data={}
        writeJson('src/sent', data)

def get_books_name(cid):
    books = loadJson('src/sent')
    result = ''
    tele = telegramLibrary()
    for book in books:
        if len(result + book + ' 作者: ' + books[book]['author']) >= 4096:
            tele.sendMessage(cid, result)
            result = ''
        result = result + book + ' 作者: ' + books[book]['author'] + '\n\n'
    tele.sendMessage(cid, result)

def find_book(bot, cid, name):
    tele = telegramLibrary()
    books = loadJson('src/sent')
    counter = 0
    for book in books:
        if name in book:
            bot.message.reply_text(f'重新傳送「 {name} 」')
            tele.sendDocumentByFileId(cid, books[book]['txt_fid'])
            counter += 1
    if counter == 0:
        bot.message.reply_text(f'找不到「 {name} 」這本書')

def send_all(cid):
    tele = telegramLibrary()
    books = loadJson('src/sent')
    for book in books:
        tele.sendDocumentByFileId(cid, books[book]['txt_fid'])

def remove_and_get_url(bot, name):
    books = loadJson('src/sent')
    try:
        book = books.pop(name)
    except Exception as e:
        bot.message.reply_text(f'找不到「 {name} 」這本書')
        return None
    
    writeJson('src/sent', books)
    return book['url']

def loadJson(path):
    with open(f'{path}.json', encoding='utf-8') as f:
        data = json.load(f)
    return data

def writeJson(path, data):
    with open(f'{path}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def findFid(res):
    return res['result']['document']['file_id']

def txt_to_epub(title):
    subprocess.run(['pandoc',
                    f'src/{title}.txt',
                    f'-o',
                    f'src/{title}.epub',
                    ])

def updateFid(title, txt_res, length, url, author):
    
    fid={'url': url,
         'author': author,
         'txt_fid': findFid(txt_res), 
         'length': str(length)}
    
    data=loadJson('src/sent')
    data[title]=fid
    writeJson('src/sent', data)
    removeDirectory(title)
    os.remove(f'src/{title}.txt')

def createDirectory(title):
    try:
        os.mkdir(f'temp/{title}')
    except:
        subprocess.run([
                        'sudo',
                        'rm',
                        '-r',
                        f'temp/{title}',
                        ])
        os.mkdir(f'temp/{title}')

def removeDirectory(title):
    os.rmdir(f'temp/{title}')

def updater(title, bot, total):
    
    if bot != None:
        msg = bot.message.reply_text(f'「 {title} 」開始下載, 0 / {total}....')
    # print(f'「 {title} 」開始下載, 0 / {total}....')
    while len(os.listdir(f'temp/{title}')) == 0:
        sleep(1)
    
    origin=0
    finish=False
    
    while len(os.listdir(f'temp/{title}')) != 0:
        sleep(2)
        temp=len(os.listdir(f'temp/{title}'))
        if origin<temp:
            if bot != None:
                msg.edit_text(f'「 {title} 」開始下載, {len(os.listdir(f"temp/{title}"))} / {total}....')
                # print(f'「 {title} 」開始下載, {len(os.listdir(f"temp/{title}"))} / {total}....')
            origin=temp
    if bot != None:
        msg.edit_text(f'「 {title} 」下載成功，總章節{total}，現在開始傳送檔案...')
    # print(f'「 {title} 」下載成功，總章節{total}，現在開始傳送檔案...')

def runFetcher(total, url, title, cid, bot):
    tele=telegramLibrary()
    createDirectory(title)   
    subprocess.Popen(['python3', 'lib/czbookFetcher.py', url, str(cid)])
    updater(title, bot, total)

def sendFileHandler(cid, url, bot=None):
    tele=telegramLibrary()
    data=loadJson('src/sent')
    downloader=czbookFetcher(url)
    title=downloader.title
    total=len(downloader.cList)
    author=downloader.author

    if title in data and data[title]['length']==str(total):
        if bot != None:
            bot.message.reply_text(f'「 {title} 」曾經下載過且沒有更新，正在傳送檔案...')
        # print(f'「 {title} 」曾經下載過且沒有更新，正在傳送檔案...')
        tele.sendDocumentByFileId(cid, data[title]['txt_fid'])
        return
    else:
        runFetcher(total, url, title, cid, bot)
        
        res = tele.sendDocument(cid, title+'.txt')
        updateFid(title, res, total, url, author)
