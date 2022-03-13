import json
import os
from lib.telegramLibrary import telegramLibrary
from lib.czbookFetcher import czbookFetcher

def getEverythingReady():
    if not os.path.exists('src'):
        os.mkdir('src')
    if not os.path.exists('temp'):
        os.mkdir('temp')
    if not os.path.exists('src/sent.json'):
        data={}
        writeJson('src/sent',data)

def loadJson(path):
    with open(f'{path}.json', encoding='utf-8') as f:
        data = json.load(f)
    return data

def writeJson(path,data):
    with open(f'{path}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def findFid(res):
    return res['result']['document']['file_id']

def updateFid(title,res):
    fid={'fid':findFid(res)}
    data=loadJson('src/sent')
    data[title]=fid
    writeJson('src/sent',data)
    os.remove(f'src/{title}.txt')
    removeDirectory(title)

def createDirectory(title):
    os.mkdir(f'temp/{title}')

def removeDirectory(title):
    os.mkdir(f'temp/{title}')

def sendFileHandler(cid,url,bot=None):
    tele=telegramLibrary()
    data=loadJson('src/sent')
    downloader=czbookFetcher(url)
    title=downloader.title

    if title in data:
        if bot != None:
            bot.message.reply_text('Novel Download Before, Send File Now!')
        tele.sendDocumentByFileId(cid,data[title]['fid'])
    else:
        createDirectory(downloader.title)
        downloader.downloader(bot,cid)
        updateFid(title,tele.sendDocument(cid,title+'.txt'))
