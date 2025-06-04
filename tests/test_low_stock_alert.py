import sys, os; sys.path.append(os.path.dirname(os.path.dirname(__file__)))
"""# tests/test_low_stock_alert.py
Test low stock alert."""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from services import inventory_service
from database import models


def test_low_stock_alert() -> None:
    async def _inner() -> None:
        engine = create_async_engine("sqlite+aiosqlite:///:memory:")
        async_session = async_sessionmaker(engine, expire_on_commit=False)
        async with engine.begin() as conn:
            await conn.run_sync(models.Base.metadata.create_all)
        async with async_session() as session:
            session.add(models.Ingredient(id=1, name="Tomato", quantity=2))
            await session.commit()
            low = await inventory_service.low_stock_alert(session, threshold=5)
            assert len(low) == 1
    asyncio.run(_inner())
