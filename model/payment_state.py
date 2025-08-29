from aiogram.fsm.state import (State, StatesGroup)

class payment_state(StatesGroup):
    wait = State()
    wait_for_validate = State()
