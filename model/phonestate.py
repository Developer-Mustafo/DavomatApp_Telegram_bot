from aiogram.fsm.state import (State, StatesGroup)

class PhoneState(StatesGroup):
    wait = State()
