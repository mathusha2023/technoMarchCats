from aiogram.fsm.state import State, StatesGroup

class AddVolunteerNewsStates(StatesGroup):  # состояние объявления для волонетров 
    heading = State()
    add_images = State()