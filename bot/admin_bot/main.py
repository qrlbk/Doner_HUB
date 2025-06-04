"""# bot/admin_bot/main.py
Admin bot entry point."""
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
import redis.asyncio as redis

from config import get_settings
from middlewares.rate_limit import AiogramRateLimitMiddleware
from . import menu_mgmt, salary, slot


def create_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    dp.message.middleware(AiogramRateLimitMiddleware())
    for module in (menu_mgmt, salary, slot):
        dp.include_router(module.router)
    return dp


def _healthcheck() -> None:
    print("ok")


async def main() -> None:
    settings = get_settings()
    bot = Bot(settings.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = create_dispatcher()
    r = await redis.from_url(settings.REDIS_URL)
    await dp.start_polling(bot)
    await r.close()


if __name__ == "__main__":
    import sys

    if "--healthcheck" in sys.argv:
        _healthcheck()
    else:
        asyncio.run(main())
