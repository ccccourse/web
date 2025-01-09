set -x

# 登入
curl -X POST http://localhost:8000/login \
     -H "Content-Type: application/json" \
     -d '{"username":"admin", "password":"password"}' \
     -c cookies.txt

# 訪問受保護路由
curl -X GET http://localhost:8000/protected \
     -b cookies.txt

# 登出
curl -X POST http://localhost:8000/logout \
     -b cookies.txt
