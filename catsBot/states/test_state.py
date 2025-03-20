from aiogram.fsm.state import State, StatesGroup


class TestStates(StatesGroup):  # состояние теста
    question1 = State()
    question2 = State()
    question3 = State()
    question4 = State()
    question5 = State()
    question6 = State()
    answer = State()
    result = State()