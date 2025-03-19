from aiogram.fsm.state import State, StatesGroup


class AdminStates(StatesGroup):
    adding_moderator = State()
    watching_moderators = State()
    delete_moderator = State()
    delete_uncommited_moderator = State()
    changing_greeting = State()
    default_answers_questions = State()
    change_questions = State()
    editing_question = State()
    adding_question = State()
    adding_answer = State()
    deleting_question = State()
