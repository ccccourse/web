# subscriber.py
import aio_pika
import asyncio
from fastapi import FastAPI

app = FastAPI()

RABBITMQ_URL = "amqp://guest:guest@localhost/"
EXCHANGE_NAME = "pub_sub_exchange"
QUEUE_NAME = "subscriber_queue"

@app.on_event("startup")
async def startup():
    asyncio.create_task(start_consumer())

async def start_consumer():
    # 連接到 RabbitMQ 並訂閱消息
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange(EXCHANGE_NAME, aio_pika.ExchangeType.FANOUT)

        # 宣告佇列並綁定交換機
        queue = await channel.declare_queue(QUEUE_NAME, durable=True)
        await queue.bind(exchange)

        print(f"Subscriber started, waiting for messages in queue: {QUEUE_NAME}")

        # 消費消息
        async for message in queue:
            async with message.process():
                print(f"Received message: {message.body.decode()}")

@app.get("/")
async def health_check():
    return {"status": "Subscriber running"}
