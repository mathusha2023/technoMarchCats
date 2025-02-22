from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from states import AddNewsStates
import keyboards
from aiogram import Router, F

router = Router()

@router.callback_query(F.data == "post_news")
async def post_news_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddNewsStates.heading)
    await callback.message.answer("Введите заголовок новости", reply_markup=keyboards.cancel_keyboard())
    await callback.answer()