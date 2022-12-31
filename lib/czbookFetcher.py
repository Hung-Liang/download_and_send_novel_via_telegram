import requests
from bs4 import BeautifulSoup
import os
import sys
from functools import partial
import multiprocessing
import re

class czbookFetcher():

    def __init__(self,url):
        self.urlPrefix='https:'
        self.getTitleAndChapter(url)

    def getTitleAndChapter(self,url):
        soup=self.getSoup(url)
        self.title=self.findElement(soup,'span','title').text.strip().replace('》','').replace('《','')
        self.author=self.findElement(soup,'span','author').a.text.strip()
        self.cList=self.getChapList(soup)

    def fetch(self,url):
        headers={'User-Agent': "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}
        resp=requests.get(url,headers=headers)
        if resp.status_code!=200:
            self.fetch(url)
        return resp.text

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
        
        soup=self.getSoup(self.urlPrefix + url[counter-1])

        if self.findElement(soup,'div','name') != None:   
            chapName=self.findElement(soup,'div','name').text.replace(self.title,'').replace('《》','')
        else:
            chapName=f'第{counter}章'

        if self.findElement(soup,'div','content') != None:
            content=self.findElement(soup,'div','content').text
        else:
            content='\n\n'

        self.makeChapterFile(counter,chapName,content)
    
    def makeChapterFile(self,counter,title,content):
        with open(f'temp/{self.title}/{counter}','w',encoding='utf-8') as f:
            f.write('# '+title+'\n\n\n\n')
        
            lines=self.find_chap_in_content(content.splitlines())
        
            for line in lines: #排版
                if line != '':
                    if '# ' in line[0:2]:
                        f.write(line.strip()+'\n\n')
                    else:
                        f.write('       '+line.strip()+'\n\n')

    def find_chap_in_content(self, lines):
        
        temp = []

        for line in lines:
            a = re.match(r'(\s+|\n|)(第)([\u4e00-\u9fa5a-zA-Z0-9]{1,7})[章節卷集部篇回][^\n]{1,35}(|\n)', line)
            if a != None:
                temp.append('# '+line.strip())
            else:
                temp.append(line)
        return temp

    def mergeChap(self,startPoint):

        with open(f'src/{self.title}.txt','a',encoding='utf-8') as f:
            
            f.write(f"% {self.title}"+'\n')
            f.write(f"% {self.author}"+'\n\n\n')

            for i in range(startPoint,len(self.cList)+1):
                f2=open(f"temp/{self.title}/{i}","r",encoding="utf-8")
                f.write(f2.read()+'\n\n\n\n\n')
                f2.close()
                os.remove(f'temp/{self.title}/{i}')

if __name__ == '__main__':

    downloader=czbookFetcher(sys.argv[1])
    cid=sys.argv[2]

    chapL=downloader.cList
    title=downloader.title
        
    pool = multiprocessing.Pool()
    pool.map(partial(downloader.getChapter,chapL), range(1,len(chapL)+1))
    pool.close()
        
    downloader.mergeChap(1)


# d = czbookFetcher('https://czbooks.net/n/ai139fl')
# print(d.author)