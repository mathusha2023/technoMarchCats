from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from states import TestStates
import keyboards
from aiogram import Router, F

router = Router()

@router.callback_query(F.data == "test")
async def test_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("""<br>1. Какой у вас образ жизни?</br>
    <br>А)</br> Спокойный, люблю проводить время дома 🙆‍♂️.
    <br>Б)</br> Активный 🏃‍♂️, часто гуляю или занимаюсь спортом.
    <br>В)</br> Занимаюсь работой или учебой 👨‍🏫, но люблю проводить время с животными.""", reply_markup=keyboards.test_reply_keyboard())
    await state.set_state(TestStates.question1)
    await state.update_data({"А": 0, "Б": 0, "В": 0})
    await callback.answer()
