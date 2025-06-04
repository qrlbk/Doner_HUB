"""Entry point for running the FastAPI application and Telegram bots."""

import asyncio

from fastapi import FastAPI
import uvicorn

from config import get_settings

# Placeholder imports for bots
# from bot.client_bot.main import start_bot as start_client_bot
# from bot.employee_bot.main import start_bot as start_employee_bot
# from bot.admin_bot.main import start_bot as start_admin_bot

app = FastAPI(title="Doner HUB")


@app.get("/")
async def read_root():
    return {"status": "ok"}


def start_api():
    """Run FastAPI application using uvicorn."""
    settings = get_settings()
    uvicorn.run(app, host="0.0.0.0", port=8000)


async def main():
    """Run API and bots concurrently."""
    # await asyncio.gather(
    #     start_client_bot(),
    #     start_employee_bot(),
    #     start_admin_bot(),
    #     start_api(),
    # )
    start_api()


if __name__ == "__main__":
    asyncio.run(main())
