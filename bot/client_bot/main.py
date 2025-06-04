"""# bot/client_bot/main.py
Client bot entry point."""
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
import redis.asyncio as redis

from config import get_settings
from middlewares.rate_limit import AiogramRateLimitMiddleware
from .handlers import router as handlers_router


def create_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    dp.message.middleware(AiogramRateLimitMiddleware())
    dp.include_router(handlers_router)
    return dp


def _healthcheck() -> None:
    print("ok")


async def main() -> None:
    settings = get_settings()
    bot = Bot(settings.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = create_dispatcher()

    r = await redis.from_url(settings.REDIS_URL)
    sub = r.pubsub()
    await sub.subscribe("order_updates")

    async def reader() -> None:
        async for msg in sub.listen():
            if msg["type"] == "message":
                await bot.send_message(settings.ADMIN_CHAT_ID, msg["data"].decode())

    await asyncio.gather(dp.start_polling(bot), reader())


if __name__ == "__main__":
    import sys

    if "--healthcheck" in sys.argv:
        _healthcheck()
    else:
        asyncio.run(main())
