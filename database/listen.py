"""# database/listen.py
Listen for Postgres notifications and publish to Redis."""
import asyncio

import asyncpg
import redis.asyncio as redis

from config import get_settings


async def main() -> None:
    settings = get_settings()
    pg = await asyncpg.connect(settings.DATABASE_URL)
    r = await redis.from_url(settings.REDIS_URL)
    await pg.add_listener("order_created", lambda *args: None)

    async def listener(conn, pid, channel, payload):
        await r.publish("order_updates", payload)

    await pg.add_listener("order_created", listener)
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
