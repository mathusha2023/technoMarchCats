from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup
from aiogram.types import Message


class StatesGroupFilter(BaseFilter):
    def __init__(self, states_group: StatesGroup):
        self.states_group = states_group

    async def __call__(self, message: Message, state: FSMContext) -> bool:
        cur_state = await state.get_state()
        return cur_state in self.states_group.__states__
