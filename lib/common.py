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

def loadJson(path):
    with open(f'{path}.json', encoding='utf-8') as f:
        data = json.load(f)
    return data

def writeJson(path, data):
    with open(f'{path}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def findFid(res):
    return res['result']['document']['file_id']

def updateFid(title, res, length):
    fid={'fid':findFid(res), 'length':str(length)}
    data=loadJson('src/sent')
    data[title]=fid
    writeJson('src/sent', data)
    removeDirectory(title)
    os.remove(f'src/{title}.txt')

def createDirectory(title):
    os.mkdir(f'temp/{title}')

def removeDirectory(title):
    os.rmdir(f'temp/{title}')

def updater(title, bot, total):
    
    if bot != None:
        msg = bot.message.reply_text(f'「 {title} 」開始下載, 0 / {total}....')
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
            origin=temp
    if bot != None:
        msg.edit_text(f'「 {title} 」下載成功，總章節{total}，現在開始傳送檔案...')

def runFetcher(total, url, title, cid, bot):
    tele=telegramLibrary()
    createDirectory(title)   
    subprocess.Popen(['python', 'lib/czbookFetcher.py', url, str(cid)])
    updater(title, bot, total)

def sendFileHandler(cid, url, bot=None):
    tele=telegramLibrary()
    data=loadJson('src/sent')
    downloader=czbookFetcher(url)
    title=downloader.title
    total=len(downloader.cList)

    if title in data and data[title]['length']==str(total):
        if bot != None:
            bot.message.reply_text(f'「 {title} 」曾經下載過且沒有更新，正在傳送檔案...')
        tele.sendDocumentByFileId(cid, data[title]['fid'])
        return
    else:
        runFetcher(total, url, title, cid, bot)

    updateFid(title, tele.sendDocument(cid, title+'.txt'), total)
