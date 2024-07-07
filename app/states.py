# states.py
from aiogram.fsm.state import StatesGroup, State

class Chat(StatesGroup):
    active = State()