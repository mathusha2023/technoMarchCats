from aiogram.fsm.state import State, StatesGroup


class WatchAnimalsStates(StatesGroup):  # Состояние просмотра животных
    watching = State()
