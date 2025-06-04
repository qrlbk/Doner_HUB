"""# middlewares/rate_limit.py
Simple rate limiting middleware."""
from __future__ import annotations

import time
from collections import defaultdict
from typing import Callable

from fastapi import Request, Response
from starlette.types import ASGIApp
from starlette.middleware.base import BaseHTTPMiddleware
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class FastAPIRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, limit: int = 10, period: int = 10) -> None:
        super().__init__(app)
        self.limit = limit
        self.period = period
        self.hits: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        ip = request.client.host
        now = time.time()
        hits = [t for t in self.hits[ip] if now - t < self.period]
        self.hits[ip] = hits
        if len(hits) >= self.limit:
            return Response(status_code=429)
        hits.append(now)
        return await call_next(request)


class AiogramRateLimitMiddleware(BaseMiddleware):
    def __init__(self, limit: int = 10, period: int = 10) -> None:
        self.limit = limit
        self.period = period
        self.hits: dict[int, list[float]] = defaultdict(list)

    async def __call__(self, handler: Callable, event: TelegramObject, data: dict):
        user_id = event.from_user.id if hasattr(event, "from_user") else 0
        now = time.time()
        hits = [t for t in self.hits[user_id] if now - t < self.period]
        self.hits[user_id] = hits
        if len(hits) >= self.limit:
            return
        hits.append(now)
        return await handler(event, data)
