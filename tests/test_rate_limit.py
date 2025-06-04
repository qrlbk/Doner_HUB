import sys, os; sys.path.append(os.path.dirname(os.path.dirname(__file__)))
"""# tests/test_rate_limit.py
Rate limit middleware tests."""
from fastapi import FastAPI
from fastapi.testclient import TestClient

from middlewares.rate_limit import FastAPIRateLimitMiddleware


def test_rate_limit() -> None:
    app = FastAPI()
    app.add_middleware(FastAPIRateLimitMiddleware, limit=2, period=1)

    @app.get("/")
    def _root() -> dict[str, str]:
        return {"ok": "ok"}

    client = TestClient(app)
    assert client.get("/").status_code == 200
    assert client.get("/").status_code == 200
    assert client.get("/").status_code == 429
