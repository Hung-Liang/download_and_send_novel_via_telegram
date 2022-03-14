# sendNovelTxtViaTelegram

- 透過Telegram將小說傳給使用者
    - 從小說狂人快速的抓取小說資料
    - 抓取相同小說的時候，除非小說有更新，否則會改用fid傳送文件，不用重複抓取

### 安裝

- 設定環境
```
pip install -r requirements.txt
```
- 設定`.env`檔案
    - 在根目錄設定檔案名為`.env`的檔案
    - 範例
    ```
    tg_token="Telegram機器人Token"
    ```


### 啟動

- `Python main.py`

### 使用方式

- `\d url` 向機器人傳送此指令來抓取小說
