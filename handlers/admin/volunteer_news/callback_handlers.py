from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from states import AddVolunteerNewsStates
import keyboards
from aiogram import Router, F

router = Router()

@router.callback_query(F.data == "volunteer_news")
async def post_news_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddVolunteerNewsStates.heading)
    await callback.message.answer("Введите заголовок новости", reply_markup=keyboards.cancel_keyboard())
    await callback.answer()