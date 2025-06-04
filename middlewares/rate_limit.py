# middlewares/rate_limit.py
"""Simple in-memory rate limiting middleware."""

from __future__ import annotations

import time
from typing import Dict, List

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

last_instance: "RateLimitMiddleware" | None = None


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Limit requests per IP address."""

    def __init__(self, app, max_requests: int = 10, window: int = 10) -> None:
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window
        self.clients: Dict[str, List[float]] = {}
        global last_instance
        last_instance = self

    def reset(self) -> None:
        """Clear stored request history."""
        self.clients.clear()

    async def dispatch(self, request: Request, call_next):
        ip = request.client.host
        now = time.time()
        history = [t for t in self.clients.get(ip, []) if t > now - self.window]
        if len(history) >= self.max_requests:
            return Response(
                status_code=429,
                content='{"detail": "Too Many Requests"}',
                media_type="application/json",
            )
        history.append(now)
        self.clients[ip] = history
        response = await call_next(request)
        return response
