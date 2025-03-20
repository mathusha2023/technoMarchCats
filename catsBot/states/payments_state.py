from aiogram.fsm.state import State, StatesGroup

class PaymentsStates(StatesGroup):  # состояния оплаты
    pricing = State()
