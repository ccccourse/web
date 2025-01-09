


## run

```
INFO:     Waiting for application startup.
INFO:     Application startup complete.
cached_item=Item 2
INFO:     127.0.0.1:50870 - "GET /items/2 HTTP/1.1" 200 OK // 上次有訪問過
cached_item=Item 2
INFO:     127.0.0.1:50870 - "GET /items/2 HTTP/1.1" 200 OK
cached_item=None
fetch_item_from_db=Item 3 # 第一次訪問 item 3, 從資料庫提取
INFO:     127.0.0.1:50871 - "GET /items/3 HTTP/1.1" 200 OK
cached_item=Item 3        # 第二次訪問 item 3, redis 中已經有了
INFO:     127.0.0.1:50873 - "GET /items/3 HTTP/1.1" 200 OK
```
