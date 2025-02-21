from aiogram.fsm.state import State, StatesGroup


class GuardianshipListAdminStates(StatesGroup):
    watching = State()
