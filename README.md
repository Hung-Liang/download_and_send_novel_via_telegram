# download_and_send_novel_via_telegram

- 透過Telegram將小說傳給使用者
  - 從小說網站快速的抓取小說資料
  - 抓取相同小說的時候，除非小說有更新，否則會改用fid傳送文件，不用重複抓取
  - 擴充性極強，可以很輕易的新增抓取其他小說網站的功能

## 安裝

- 設定環境

```cmd
pip install -r requirements.txt
```

- 設定`.env`檔案
  - 在根目錄設定檔案名為`.env`的檔案
  - 請參考`.env.example`的格式以及內容

## 啟動

- `Python main.py`

## 使用方式

- `\d url` 向機器人傳送此指令來抓取小說

## Disclaimer

- 此專案僅供學術研究使用，請勿用於任何商業用途
- 此專案僅提供為爬蟲學習使用，請勿用於任何非法用途
