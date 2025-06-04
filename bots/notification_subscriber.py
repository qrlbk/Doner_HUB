# bots/notification_subscriber.py
"""Redis subscriber forwarding notifications to bots."""

import asyncio

import redis.asyncio as redis

from config import get_settings


async def main() -> None:
    r = redis.from_url(get_settings().REDIS_URL)
    pubsub = r.pubsub()
    await pubsub.subscribe("order_created", "low_stock")
    async for message in pubsub.listen():
        if message.get("type") == "message":
            print("Notification:", message.get("data"))


if __name__ == "__main__":
    asyncio.run(main())
