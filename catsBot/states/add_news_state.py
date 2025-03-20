from aiogram.fsm.state import State, StatesGroup

class AddNewsStates(StatesGroup):  # класс состояний для добавления новости
    heading = State()
    add_images = State()