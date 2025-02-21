from aiogram.fsm.state import State, StatesGroup


class UpdateAnimalStates(StatesGroup):
    index_input = State()
    choose_change_param = State()
    naming = State()
    changing_gender = State()
    changing_birthday = State()
    describing = State()
    changing_images = State()
    changing_tags = State()
