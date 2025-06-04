# database/listener.py
"""PostgreSQL LISTEN/NOTIFY forwarder."""

import asyncio

import asyncpg
import redis.asyncio as redis

from config import get_settings


async def _notify(conn, pid, channel, payload) -> None:
    r = redis.from_url(get_settings().REDIS_URL)
    await r.publish("order_created", payload)
    await r.close()


async def main() -> None:
    settings = get_settings()
    conn = await asyncpg.connect(settings.DATABASE_URL)
    await conn.add_listener("orders_channel", _notify)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
