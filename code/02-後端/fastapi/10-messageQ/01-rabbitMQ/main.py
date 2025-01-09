from fastapi import FastAPI
import aio_pika
import asyncio

app = FastAPI()

RABBITMQ_URL = "amqp://guest:guest@localhost/"  # RabbitMQ 的 URL

@app.on_event("startup")
async def setup_rabbitmq():
    # 建立連線
    app.state.rabbit_connection = await aio_pika.connect_robust(RABBITMQ_URL)
    app.state.rabbit_channel = await app.state.rabbit_connection.channel()
    app.state.rabbit_queue = await app.state.rabbit_channel.declare_queue("my_queue", durable=True)

@app.on_event("shutdown")
async def shutdown_rabbitmq():
    await app.state.rabbit_connection.close()

@app.post("/publish/")
async def publish_message(message: str):
    # 發送訊息
    await app.state.rabbit_channel.default_exchange.publish(
        aio_pika.Message(body=message.encode()),
        routing_key="my_queue"
    )
    return {"status": "Message sent!"}

# 消費者：處理佇列中的訊息
async def consume_messages():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("my_queue", durable=True)

        async for message in queue:
            async with message.process():
                print(f"Received message: {message.body.decode()}")

# 啟動消費者
@app.on_event("startup")
async def start_consumer():
    asyncio.create_task(consume_messages())
