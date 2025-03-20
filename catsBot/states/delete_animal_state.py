from aiogram.fsm.state import State, StatesGroup


class DeleteAnimalStates(StatesGroup):  # состояния удаления животного
    index_input = State()
    confirm_delete = State()
