"""# bot/employee_bot/states.py
Employee bot FSM states."""
from aiogram.fsm.state import State, StatesGroup


class WorkStates(StatesGroup):
    idle = State()
    processing_order = State()
