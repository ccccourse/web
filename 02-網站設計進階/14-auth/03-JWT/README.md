
啟動 server

    fastapi dev main.py

測試

```
% ./test.sh
=== 用戶註冊 ===
{"message":"User registered successfully"}
=== 用戶登入 ===

=== 公開路由 ===
{"message":"這是公開路由"}
=== 受保護路由 ===
{"username":"testuser","email":"test@example.com","disabled":false}
=== 使用錯誤 Token ===
{"detail":"Could not validate credentials"}%   
```
