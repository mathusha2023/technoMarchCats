from aiogram.fsm.state import State, StatesGroup


class UsersControlStates(StatesGroup):  # Класс состояний контроля пользоваелей 
    searching_by_username = State()
