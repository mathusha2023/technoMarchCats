from aiogram.fsm.state import State, StatesGroup


class GuardianshipListAdminStates(StatesGroup):  # Состояния администратора просмотра заявок на животое
    watching = State()
