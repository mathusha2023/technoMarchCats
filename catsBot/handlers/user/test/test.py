from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from states import TestStates
import keyboards
from aiogram import Router, F

router = Router()

@router.callback_query(F.data == "test")
async def test_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("""<b>1. Какой у вас образ жизни?</b>
    <b>1.</b> Спокойный, люблю проводить время дома.
    <b>2.</b> Активный ️, часто гуляю или занимаюсь спортом.
    <b>3.</b> Занимаюсь работой или учебой, но люблю проводить время с животными.""", reply_markup=keyboards.test_reply_keyboard())
    await state.set_state(TestStates.question1)
    await state.update_data({"1": 0, "2": 0, "3": 0})
    await callback.answer()
