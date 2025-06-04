"""# services/menu_service.py
Menu management services."""
from dataclasses import dataclass
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import models


@dataclass
class DishData:
    name: str
    price: float
    visible: bool = True


async def create_dish(session: AsyncSession, data: DishData) -> models.Dish:
    dish = models.Dish(**data.__dict__)
    session.add(dish)
    await session.commit()
    await session.refresh(dish)
    return dish


async def list_dishes(session: AsyncSession) -> Iterable[models.Dish]:
    result = await session.execute(select(models.Dish))
    return result.scalars().all()


async def toggle_visible(session: AsyncSession, dish_id: int) -> None:
    dish = await session.get(models.Dish, dish_id)
    dish.visible = not dish.visible
    await session.commit()
