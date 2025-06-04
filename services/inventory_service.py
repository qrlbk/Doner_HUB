"""# services/inventory_service.py
Inventory management services."""
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import models


async def apply_stock_moves(session: AsyncSession, moves: list[models.StockMove]) -> None:
    for move in moves:
        session.add(move)
    await session.commit()


async def low_stock_alert(session: AsyncSession, threshold: float) -> list[models.Ingredient]:
    stmt = select(models.Ingredient).where(models.Ingredient.quantity < threshold)
    res = await session.execute(stmt)
    return res.scalars().all()
