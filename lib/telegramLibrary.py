import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

class telegramLibrary():

    def __init__(self):
        self.token=os.environ.get("tg_token")
    
    def sendMessage(self,cid,message):
        url = f'https://api.telegram.org/bot{self.token}/sendMessage?chat_id={cid}&parse_mode=HTML&text={message}' 
        requests.get(url)

    def sendDocument(self,cid,filename,path='src/'):
        files = {
                "document": (filename,open(f'{path}{filename}','rb'), 'application/octet-stream'),
                }
        url = f'https://api.telegram.org/bot{self.token}/sendDocument?chat_id={cid}' 
        res=requests.post(url,files=files)
        return json.loads(res.text)
    
    def sendDocumentByFileId(self,cid,fileId):
        url = f'https://api.telegram.org/bot{self.token}/sendDocument?chat_id={cid}&document={fileId}' 
        res=requests.post(url)
    
    def getMessage(self):
        url = f'https://api.telegram.org/bot{self.token}/getUpdates'
        data={'offset':-1}
        res=requests.post(url,data=data)
