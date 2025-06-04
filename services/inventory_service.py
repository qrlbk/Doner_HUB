# services/inventory_service.py
"""Service helpers for tracking stock movements and ingredients."""

from __future__ import annotations

from typing import Dict, List

import redis.asyncio as redis

from config import get_settings
from services.menu_service import _DISHES
from services.order_service import _ORDER_ITEMS

# ingredient_id -> {qty, min_qty}
_STOCK: Dict[int, Dict[str, float]] = {
    1: {"qty": 5.0, "min_qty": 2.0},
    2: {"qty": 3.0, "min_qty": 1.0},
}

# dish_id -> {ingredient_id: qty}
_DISH_INGREDIENTS: Dict[int, Dict[int, float]] = {
    1: {1: 1.0, 2: 0.5},
    2: {1: 0.5},
}


async def apply_stock_moves(order_id: str) -> List[int]:
    """Apply stock changes for order items."""
    low_stock: List[int] = []
    for item in [i for i in _ORDER_ITEMS if i["order_id"] == order_id]:
        ingredients = _DISH_INGREDIENTS.get(item["dish_id"], {})
        for ing_id, qty in ingredients.items():
            stock = _STOCK.setdefault(ing_id, {"qty": 0.0, "min_qty": 0.0})
            stock["qty"] -= qty * item.get("qty", 1)
            if stock["qty"] < stock.get("min_qty", 0):
                low_stock.append(ing_id)
    return low_stock


async def low_stock_alert(low_stock_ids: List[int]) -> None:
    """Publish low stock ids to redis channel."""
    if not low_stock_ids:
        return
    r = redis.from_url(get_settings().REDIS_URL)
    for ing in low_stock_ids:
        await r.publish("low_stock", str(ing))
    await r.close()
