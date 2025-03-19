from aiogram.fsm.state import State, StatesGroup

class AddNewsStates(StatesGroup):
    heading = State()
    add_images = State()