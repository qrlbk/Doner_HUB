import sys, os; sys.path.append(os.path.dirname(os.path.dirname(__file__)))
"""# tests/test_create_order.py
Test order creation flow."""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from services import order_service
from database import models


def test_create_order() -> None:
    async def _inner() -> None:
        engine = create_async_engine("sqlite+aiosqlite:///:memory:")
        async_session = async_sessionmaker(engine, expire_on_commit=False)
        async with engine.begin() as conn:
            await conn.run_sync(models.Base.metadata.create_all)
        async with async_session() as session:
            cmd = order_service.CreateOrderCommand(user_id=1, items=[(1, 2)])
            order = await order_service.create_order(session, cmd)
            assert order.id == 1
    asyncio.run(_inner())
