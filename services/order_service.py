# services/order_service.py
"""Service layer for working with orders."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional
from uuid import uuid4


@dataclass
class OrderDTO:
    """Data returned when listing orders."""

    id: str
    user_id: int
    status: str
    items: List[dict]


_ORDERS: Dict[str, OrderDTO] = {}
_ORDER_ITEMS: List[dict] = []


async def create_order(user_id: int, items: List[dict]) -> str:
    """Create order and related items in one transaction."""
    order_id = str(uuid4())
    dto = OrderDTO(id=order_id, user_id=user_id, status="new", items=items)
    _ORDERS[order_id] = dto
    for item in items:
        _ORDER_ITEMS.append({"order_id": order_id, **item})
    return order_id


async def list_orders(status: Optional[str] = None) -> List[OrderDTO]:
    """Return orders filtered by status."""
    values = list(_ORDERS.values())
    if status:
        values = [o for o in values if o.status == status]
    return values
