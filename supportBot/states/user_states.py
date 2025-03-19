from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    asking_question = State()
    voting = State()
