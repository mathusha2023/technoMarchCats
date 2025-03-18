from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from states import TestStates
import keyboards
from aiogram import Router, F
from utils.best_match import best_match 

router = Router()

results = {
        "А": ["Спокойный", "Ласковый", "Послушный", "Домашний", "Серый", "Дымчатый"],
        "Б": ["Игривый", "Активный", "Любопытный", "Рыжий", "Полосатый", "Пушистый"],
        "В": ["Гордый", "Неприступный", "Непривередливый", "Черный", "Белый", "Пятнистый"]
    }

@router.callback_query(F.data.in_(["А", "Б", "В"]), TestStates.question1)
async def question1(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data[callback.data] += 1
    await state.update_data(data)
    await callback.message.answer("""2. Какой характер кота вам ближе?
    А) Спокойный и ласковый.
    Б) Игривый и любопытный.
    В) Независимый и гордый.""", reply_markup=keyboards.test_keyboard())
    await state.set_state(TestStates.question2)
    await callback.answer()

@router.callback_query(F.data.in_(["А", "Б", "В"]), TestStates.question2)
async def question2(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data[callback.data] += 1
    await callback.message.answer("""3. Сколько времени вы готовы уделять коту?
    А) Много времени, готов(а) играть и ухаживать.
    Б) Умеренно, но регулярно.
    В) Немного, но готов(а) обеспечить комфорт.""", reply_markup=keyboards.test_keyboard())
    await state.set_state(TestStates.question3)
    await callback.answer()

@router.callback_query(F.data.in_(["А", "Б", "В"]), TestStates.question3)
async def question3(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data[callback.data] += 1
    await callback.message.answer("""4. Какой окрас кота вам нравится?
    А) Серый, дымчатый, черный.
    Б) Рыжий, полосатый, пятнистый.
    В) Белый, пушистый.""", reply_markup=keyboards.test_keyboard())
    await state.set_state(TestStates.question4)
    await callback.answer()

@router.callback_query(F.data.in_(["А", "Б", "В"]), TestStates.question4)
async def question4(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data[callback.data] += 1
    await callback.message.answer("""5. Какой темперамент кота вам подходит?
    А) Миролюбивый и послушный.
    Б) Активный и любопытный.
    В) Независимый и неприступный.""", reply_markup=keyboards.test_keyboard())
    await state.set_state(TestStates.question5)
    await callback.answer()

@router.callback_query(F.data.in_(["А", "Б", "В"]), TestStates.question5)
async def question5(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data[callback.data] += 1
    await callback.message.answer("""6. Есть ли у вас дети или другие животные?
    А) Да, нужен кот, который ладит с другими.
    Б) Нет, но хочу, чтобы кот был дружелюбным.
    В) Нет, предпочитаю кота, который не требует много внимания.""", reply_markup=keyboards.test_keyboard())
    await state.set_state(TestStates.question6)
    await callback.answer()

@router.callback_query(F.data.in_(["А", "Б", "В"]), TestStates.question6)
async def question6(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data[callback.data] += 1
    await callback.message.answer("""7. Готовы ли вы ухаживать за котом, который нуждается в лечении?
    А) Да, готов(а) помочь.
    Б) Нет, предпочитаю здорового кота.
    В) Возможно, если это не требует больших усилий.""", reply_markup=keyboards.test_keyboard())
    await state.set_state(TestStates.answer)
    await callback.answer()

@router.callback_query(F.data.in_(["А", "Б", "В"]), TestStates.answer)
async def answer(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.answer(f"вам подойдет котик {best_match(results[max(data, key=data.get)])}")
    await message.answer(strings.GREETING, reply_markup=keyboards.start_keyboard())
    await state.clear()