"""Entry point for running the FastAPI application and Telegram bots."""

import asyncio

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from middlewares.rate_limit import RateLimitMiddleware
from services import inventory_service, order_service

app = FastAPI(title="Doner HUB")
rate_limiter = RateLimitMiddleware(app, max_requests=10, window=10)
app.add_middleware(RateLimitMiddleware, max_requests=10, window=10)


class OrderItem(BaseModel):
    dish_id: int
    qty: int
    price: float


class OrderCreate(BaseModel):
    user_id: int
    items: list[OrderItem]


@app.get("/")
async def read_root() -> dict:
    return {"status": "ok"}


@app.get("/health")
async def health() -> dict:
    """Healthcheck endpoint."""
    return {"status": "ok"}


@app.post("/orders", status_code=201)
async def create_order(payload: OrderCreate) -> dict:
    order_id = await order_service.create_order(
        payload.user_id,
        [item.dict() for item in payload.items],
    )
    await inventory_service.apply_stock_moves(order_id)
    return {"order_id": order_id}


def start_api() -> None:
    """Run FastAPI application using uvicorn."""
    uvicorn.run(app, host="0.0.0.0", port=8000)


async def main() -> None:
    """Run API (bots stubs are commented)."""
    start_api()


if __name__ == "__main__":
    asyncio.run(main())
