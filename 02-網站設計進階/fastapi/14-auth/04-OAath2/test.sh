#!/bin/bash

# 基本 URL
BASE_URL="http://127.0.0.1:8000"

# 主頁測試
echo "=== 測試主頁 ==="
curl $BASE_URL/

# 公開路由測試
echo -e "\n=== 公開路由 ==="
curl $BASE_URL/public

# Google 登入重定向（注意：瀏覽器更適合此測試）
echo -e "\n=== Google 登入重定向 ==="
curl -L $BASE_URL/login/google