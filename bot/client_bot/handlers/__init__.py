"""# bot/client_bot/handlers/__init__.py
Client bot handlers package."""
from aiogram import Router

from . import menu

router = Router()
router.include_router(menu.router)
