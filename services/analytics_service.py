"""# services/analytics_service.py
Analytics helpers."""
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from database import models


daily_revenue_mv = text("REFRESH MATERIALIZED VIEW CONCURRENTLY daily_revenue_mv")


async def refresh_daily_revenue(session: AsyncSession) -> None:
    await session.execute(daily_revenue_mv)
    await session.commit()


async def top_dishes(session: AsyncSession, limit: int = 5) -> list[tuple[str, int]]:
    stmt = (
        select(models.Dish.name, func.count(models.OrderItem.id))
        .join(models.OrderItem, models.OrderItem.dish_id == models.Dish.id)
        .group_by(models.Dish.name)
        .order_by(func.count(models.OrderItem.id).desc())
        .limit(limit)
    )
    res = await session.execute(stmt)
    return res.all()
