
## 測試

key 正確，通過

```
$ curl -H "X-API-Key: secret_api_key" http://127.0.0.1:8000/secure-api-key-header

{"message":"Access granted"}
```

key 錯誤，不通過

```
$ curl -H "X-API-Key: wrong_api_key" http://127.0.0.1:8000/secure-api-key-header

{"detail":"Invalid API Key"}                

```