"""# bot/client_bot/states.py
FSM states for client orders."""
from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    choosing_dish = State()
    choosing_quantity = State()
