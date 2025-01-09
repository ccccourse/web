# curl -X POST "http://127.0.0.1:8000/publish/" -H "Content-Type: application/json" -d '{"message": "Hello RabbitMQ!"}'

curl -X POST "http://127.0.0.1:8000/publish/?message=Hello%20RabbitMQ"
