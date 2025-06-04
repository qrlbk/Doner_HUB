import pathlib
import sys

import pytest
from httpx import ASGITransport, AsyncClient

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from run import app
from services import inventory_service


@pytest.mark.asyncio
async def test_create_order():
    items = [{"dish_id": 1, "qty": 1, "price": 10.0}]
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post("/orders", json={"user_id": 1, "items": items})
    assert resp.status_code == 201
    order_id = resp.json()["order_id"]

    before = inventory_service._STOCK[1]["qty"]
    low = await inventory_service.apply_stock_moves(order_id)
    assert inventory_service._STOCK[1]["qty"] == before - 1.0
    assert isinstance(low, list)
