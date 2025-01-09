# api-key

訪問

http://127.0.0.1:8000/secure-api-key?api_key=secret_api_key

可通過，傳回

    {"message":"Access granted"}

api_key 錯誤則無法通過，傳回

    {"detail":"Invalid API Key"}
