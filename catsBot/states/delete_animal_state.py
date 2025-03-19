from aiogram.fsm.state import State, StatesGroup


class DeleteAnimalStates(StatesGroup):
    index_input = State()
    confirm_delete = State()
