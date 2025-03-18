from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from states import TestStates
import keyboards
from aiogram import Router, F

router = Router()

@router.message(F.text, TestStates.question1)
async def post_news_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("""2. Какой характер кота вам ближе?
    А) Спокойный и ласковый.
    Б) Игривый и любопытный.
    В) Независимый и гордый.""", reply_markup=keyboards.test_keyboard())
    await state.set_state(TestStates.question2)
    await callback.answer()

@router.message(F.text, TestStates.question2)
async def post_news_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("""3. Сколько времени вы готовы уделять коту?
    А) Много времени, готов(а) играть и ухаживать.
    Б) Умеренно, но регулярно.
    В) Немного, но готов(а) обеспечить комфорт.""", reply_markup=keyboards.test_keyboard())
    await state.set_state(TestStates.question3)
    await callback.answer()

@router.message(F.text, TestStates.question3)
async def post_news_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(TestStates.question3)
    await callback.message.answer("""4. Какой окрас кота вам нравится?
    А) Серый, дымчатый, черный.
    Б) Рыжий, полосатый, пятнистый.
    В) Белый, пушистый.""", reply_markup=keyboards.test_keyboard())
    await state.set_state(TestStates.question4)
    await callback.answer()

@router.message(F.text, TestStates.question4)
async def post_news_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(TestStates.question4)
    await callback.message.answer("""5. Какой темперамент кота вам подходит?
    А) Миролюбивый и послушный.
    Б) Активный и любопытный.
    В) Независимый и неприступный.""", reply_markup=keyboards.test_keyboard())
    await state.set_state(TestStates.question5)
    await callback.answer()
    
@router.message(F.text, TestStates.question5)
async def post_news_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(TestStates.question4)
    await callback.message.answer("""6. Есть ли у вас дети или другие животные?
    А) Да, нужен кот, который ладит с другими.
    Б) Нет, но хочу, чтобы кот был дружелюбным.
    В) Нет, предпочитаю кота, который не требует много внимания.""", reply_markup=keyboards.test_keyboard())
    await state.set_state(TestStates.question6)
    await callback.answer()
    
@router.message(F.text, TestStates.question6)
async def post_news_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(TestStates.question4)
    await callback.message.answer("""7. Готовы ли вы ухаживать за котом, который нуждается в лечении?
    А) Да, готов(а) помочь.
    Б) Нет, предпочитаю здорового кота.
    В) Возможно, если это не требует больших усилий.""", reply_markup=keyboards.test_keyboard())
    await state.clear_state()
    await callback.answer()