import aio_pika
import asyncio
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

RABBITMQ_URL = "amqp://guest:guest@localhost/"
EXCHANGE_NAME = "pub_sub_exchange"


@app.on_event("startup")
async def startup():
    # 建立與 RabbitMQ 的連線
    app.state.rabbit_connection = await aio_pika.connect_robust(RABBITMQ_URL)
    app.state.channel = await app.state.rabbit_connection.channel()

    # 宣告交換機
    app.state.exchange = await app.state.channel.declare_exchange(
        EXCHANGE_NAME, aio_pika.ExchangeType.FANOUT
    )


@app.on_event("shutdown")
async def shutdown():
    # 關閉 RabbitMQ 連線
    await app.state.rabbit_connection.close()


@app.post("/publish/")
async def publish_message(message: str):
    """
    發佈消息到 RabbitMQ 交換機
    """
    await app.state.exchange.publish(
        aio_pika.Message(body=message.encode()),
        routing_key="",  # FANOUT 類型交換機不需要指定 routing key
    )
    return {"status": "Message published!", "message": message}


async def consume_messages(queue_name: str):
    """
    訂閱者：接收 RabbitMQ 訊息
    """
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()

        # 宣告交換機與佇列
        exchange = await channel.declare_exchange(EXCHANGE_NAME, aio_pika.ExchangeType.FANOUT)
        queue = await channel.declare_queue(queue_name, durable=True)
        await queue.bind(exchange)

        print(f"Subscribed to queue: {queue_name}")

        # 消費訊息
        async for message in queue:
            async with message.process():
                print(f"Received message: {message.body.decode()}")


@app.on_event("startup")
async def start_subscriber():
    """
    啟動兩個模擬的訂閱者，分別監聽不同的佇列
    """
    asyncio.create_task(consume_messages("subscriber_1"))
    asyncio.create_task(consume_messages("subscriber_2"))
