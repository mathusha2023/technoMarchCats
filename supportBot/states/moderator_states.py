from aiogram.fsm.state import State, StatesGroup


class ModeratorStates(StatesGroup):
    answering_question = State()

