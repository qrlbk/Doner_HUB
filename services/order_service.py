"""# services/order_service.py
Order related service functions."""
from dataclasses import dataclass
from typing import Iterable

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import models


@dataclass
class CreateOrderCommand:
    user_id: int
    items: list[tuple[int, int]]  # list of (dish_id, quantity)


async def create_order(session: AsyncSession, cmd: CreateOrderCommand) -> models.Order:
    """Create order with items."""
    order = models.Order(user_id=cmd.user_id)
    session.add(order)
    await session.flush()
    for dish_id, quantity in cmd.items:
        item = models.OrderItem(order_id=order.id, dish_id=dish_id, quantity=quantity)
        session.add(item)
    await session.commit()
    await session.refresh(order)
    return order


async def list_orders(session: AsyncSession, user_id: int | None = None) -> Iterable[models.Order]:
    """Return orders optionally filtered by user."""
    stmt = select(models.Order).order_by(models.Order.created_at.desc())
    if user_id:
        stmt = stmt.where(models.Order.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalars().all()
