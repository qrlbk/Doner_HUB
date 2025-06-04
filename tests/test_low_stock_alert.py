import pathlib
import sys

import pytest

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from services import inventory_service


class DummyRedis:
    def __init__(self) -> None:
        self.published = []

    async def publish(self, channel: str, data: str):
        self.published.append((channel, data))

    async def close(self):
        pass


@pytest.mark.asyncio
async def test_low_stock_alert(monkeypatch):
    dummy = DummyRedis()
    monkeypatch.setattr(inventory_service.redis, "from_url", lambda *_a, **_k: dummy)
    await inventory_service.low_stock_alert([1, 2])
    assert ("low_stock", "1") in dummy.published
    assert ("low_stock", "2") in dummy.published
