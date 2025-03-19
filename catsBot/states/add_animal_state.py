from aiogram.fsm.state import State, StatesGroup


class AddAnimalStates(StatesGroup):
    naming = State()
    adding_gender = State()
    adding_birthday = State()
    describing = State()
    adding_images = State()
    adding_tags = State()
    confirm_adding = State()
