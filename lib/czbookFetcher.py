import requests
from bs4 import BeautifulSoup
import os

class czbookFetcher():

    def __init__(self,url):
        self.urlPrefix='https:'
        self.getTitleAndChapter(url)

    def getTitleAndChapter(self,url):
        soup=self.getSoup(url)
        self.title=self.findElement(soup,'span','title').text.strip().replace('》','').replace('《','')
        self.cList=self.getChapList(soup)

    def fetch(self,url):
        headers={'User-Agent': "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}
        resp=requests.get(url,headers=headers).text
        return resp

    def getChapList(self,soup): #找出網頁的章節連結
        cList=[]
        for t in soup.find('ul','nav chapter-list').find_all('a'):
            cList.append(t.get('href'))
        return cList

    def getSoup(self,url):
        return BeautifulSoup(self.fetch(url), 'lxml')

    def findElement(self,soup,classTag,className):
        return soup.find(classTag,className)

    def getChapter(self,url,counter):
        soup=self.getSoup(self.urlPrefix + url)
        chapName=self.findElement(soup,'div','name').text.replace(self.title,'').replace('《》','')
        content=self.findElement(soup,'div','content').text
        self.makeChapterFile(counter,chapName,content)
    
    def makeChapterFile(self,counter,title,content):
        with open(f'temp/{self.title}/{counter}','w',encoding='utf-8') as f:
            f.write(title+'\n\n\n\n')
            lines=content.splitlines()
            for line in lines: #排版
                if line != '':
                    f.write('       '+line.strip()+'\n\n')
    
    def mergeChap(self):

        with open(f'src/{self.title}.txt','a',encoding='utf-8') as f:
            for i in range(0,len(self.cList)):
                f2=open(f"temp/{self.title}/{i+1}","r",encoding="utf-8")
                f.write(f2.read()+'\n\n\n\n\n')
                f2.close()
                os.remove(f'temp/{self.title}/{i+1}')

    def downloader(self,bot=None,cid=None,startPoint=1):
        
        chapterLen=len(self.cList)

        counter=startPoint

        if bot!=None:
            msg = bot.message.reply_text(f'「 {self.title} 」開始下載')

        for i in range(counter-1,len(self.cList)):
            self.getChapter(self.cList[i],counter)
            
            if msg!=None:
                msg.edit_text(f'「 {self.title} 」開始下載, {counter} / {chapterLen}....')

            counter+=1

        self.mergeChap()        
        msg.edit_text(f'「 {self.title} 」下載成功，總章節{chapterLen}，現在開始傳送檔案...')





	