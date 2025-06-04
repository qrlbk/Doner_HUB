"""# api/router.py
FastAPI API router."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services import analytics_service, menu_service, order_service
from database.models import Base

router = APIRouter()


async def get_session() -> AsyncSession:
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

    from config import get_settings

    settings = get_settings()
    engine = create_async_engine(settings.DATABASE_URL, future=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session


@router.post("/orders")
async def create_order(cmd: order_service.CreateOrderCommand, session: AsyncSession = Depends(get_session)):
    order = await order_service.create_order(session, cmd)
    return {"order_id": order.id}


@router.get("/orders")
async def list_orders(session: AsyncSession = Depends(get_session)):
    orders = await order_service.list_orders(session)
    return [o.id for o in orders]


@router.get("/menu")
async def list_menu(session: AsyncSession = Depends(get_session)):
    dishes = await menu_service.list_dishes(session)
    return [{"id": d.id, "name": d.name} for d in dishes]


@router.get("/analytics/top-dishes")
async def top_dishes(session: AsyncSession = Depends(get_session)):
    return await analytics_service.top_dishes(session)
