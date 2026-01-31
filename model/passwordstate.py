from aiogram.fsm.state import (State, StatesGroup)

class PasswordState(StatesGroup):
    wait = State()
    password = State()
