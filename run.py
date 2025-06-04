"""# run.py
FastAPI application startup."""
import asyncio
from fastapi import FastAPI
import uvicorn

from api.router import router
from middlewares.rate_limit import FastAPIRateLimitMiddleware
from config import get_settings

app = FastAPI(title="Doner HUB")
app.add_middleware(FastAPIRateLimitMiddleware)
app.include_router(router)


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"status": "ok"}


def start_api() -> None:
    settings = get_settings()
    uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=False)


async def main() -> None:
    start_api()


if __name__ == "__main__":
    asyncio.run(main())
