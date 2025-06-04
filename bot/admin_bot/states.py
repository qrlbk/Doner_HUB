"""# bot/admin_bot/states.py
Admin bot FSM states."""
from aiogram.fsm.state import State, StatesGroup


class AdminStates(StatesGroup):
    menu = State()
    salary = State()
