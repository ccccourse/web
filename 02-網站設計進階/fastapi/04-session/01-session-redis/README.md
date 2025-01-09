
## 來源

本程式由 claude 產生

https://claude.ai/chat/14f549be-ed17-4e6a-8d94-b4642f6b24ba

## 啟動

    fastapi dev main.py

## 測試

```sh
(base) cccimac@cccimacdeiMac 01-session-claude % ./test.sh
+ curl -X POST http://localhost:8000/login -H 'Content-Type: application/json' -d '{"username":"admin", "password":"password"}' -c cookies.txt
{"message":"Login successful"}+ curl -X GET http://localhost:8000/protected -b cookies.txt
{"message":"Welcome, admin!"}+ curl -X POST http://localhost:8000/logout -b cookies.txt
{"message":"Logged out successfully"}
```
