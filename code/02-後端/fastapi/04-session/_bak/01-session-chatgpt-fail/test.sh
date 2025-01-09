set -x

curl -X POST "http://127.0.0.1:8000/login" -d "username=admin&password=1234" -c cookies.txt

curl -X GET "http://127.0.0.1:8000/secure-endpoint" -b cookies.txt

curl -X POST "http://127.0.0.1:8000/logout" -b cookies.txt -c cookies.txt

curl -X GET "http://127.0.0.1:8000/secure-endpoint" -b cookies.txt


#curl -X POST "http://127.0.0.1:8000/login" -d "username=admin&password=1234"

#curl -X GET "http://127.0.0.1:8000/secure-endpoint" -b "session_id=<your_session_id>"

#curl -X POST "http://127.0.0.1:8000/logout" -b "session_id=<your_session_id>"
