from aiogram.fsm.state import State, StatesGroup

class AddVolunteerNewsStates(StatesGroup):
    heading = State()
    add_images = State()