from aiogram.fsm.state import (State, StatesGroup)

class ImageState(StatesGroup):
    wait = State()
    wait_for_validate = State()
