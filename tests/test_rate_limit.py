import pathlib
import sys

import pytest
from httpx import ASGITransport, AsyncClient

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from middlewares import rate_limit
from run import app


@pytest.mark.asyncio
async def test_rate_limit():
    if rate_limit.last_instance:
        rate_limit.last_instance.reset()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        for _ in range(10):
            r = await ac.get("/health")
            assert r.status_code == 200
        resp = await ac.get("/health")
        assert resp.status_code == 429
