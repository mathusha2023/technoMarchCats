from aiogram.fsm.state import State, StatesGroup

class PaymentsStates(StatesGroup):
    pricing = State()
