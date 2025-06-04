"""# bot/client_bot/handlers/menu.py
Menu commands for client bot."""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("menu"))
async def show_menu(message: Message) -> None:
    await message.answer("Menu is empty")
