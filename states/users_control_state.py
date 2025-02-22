from aiogram.fsm.state import State, StatesGroup


class UsersControlStates(StatesGroup):
    searching_by_username = State()
