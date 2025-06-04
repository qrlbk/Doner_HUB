"""# bot/employee_bot/auth.py
Handlers for employee authentication."""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def start(message: Message) -> None:
    await message.answer("Employee bot")
