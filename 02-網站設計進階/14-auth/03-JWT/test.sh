#!/bin/bash

# 基本 URL
BASE_URL="http://127.0.0.1:8000"

# 用戶註冊
echo "=== 用戶註冊 ==="
curl -X POST $BASE_URL/register \
     -H "Content-Type: application/json" \
     -d '{"username":"testuser", "password":"strongpassword", "email":"test@example.com"}'

# 用戶登入
echo -e "\n=== 用戶登入 ==="
TOKEN_RESPONSE=$(curl -s -X POST $BASE_URL/token \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=testuser&password=strongpassword")

# 提取 Token
TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.access_token')

# 訪問公開路由
echo -e "\n=== 公開路由 ==="
curl $BASE_URL/public

# 訪問受保護路由
echo -e "\n=== 受保護路由 ==="
curl $BASE_URL/users/me \
     -H "Authorization: Bearer $TOKEN"

# 嘗試使用錯誤 Token
echo -e "\n=== 使用錯誤 Token ==="
curl $BASE_URL/users/me \
     -H "Authorization: Bearer WRONG_TOKEN"