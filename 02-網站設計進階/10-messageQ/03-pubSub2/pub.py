# publisher.py
import aio_pika
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

RABBITMQ_URL = "amqp://guest:guest@localhost/"
EXCHANGE_NAME = "pub_sub_exchange"

class MessageBody(BaseModel):
    message: str

@app.on_event("startup")
async def startup():
    # 建立 RabbitMQ 連線和交換機
    app.state.rabbit_connection = await aio_pika.connect_robust(RABBITMQ_URL)
    app.state.channel = await app.state.rabbit_connection.channel()
    app.state.exchange = await app.state.channel.declare_exchange(
        EXCHANGE_NAME, aio_pika.ExchangeType.FANOUT
    )

@app.on_event("shutdown")
async def shutdown():
    await app.state.rabbit_connection.close()

@app.post("/publish/")
async def publish_message(body: MessageBody):
    # 發佈消息到交換機
    message = body.message
    await app.state.exchange.publish(
        aio_pika.Message(body=message.encode()),
        routing_key=""
    )
    return {"status": "Message published!", "message": message}
