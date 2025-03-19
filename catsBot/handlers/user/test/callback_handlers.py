from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from states import TestStates
import keyboards
from aiogram import Router, F
from utils.best_match import best_match
from utils.generate_animal_card_by_state import generate_animal_card_by_state
from utils.main_info import get_animal_info
import strings
from filters import StatesGroupFilter

router = Router()

results = {
        "1️⃣": ["Спокойный", "Ласковый", "Послушный", "Домашний", "Серый", "Дымчатый"],
        "2️⃣": ["Игривый", "Активный", "Любопытный", "Рыжий", "Полосатый", "Пушистый"],
        "3️⃣": ["Гордый", "Неприступный", "Непривередливый", "Черный", "Белый", "Пятнистый"]
    }

@router.message(F.text == "🚫 Отмена",
                StatesGroupFilter(TestStates))  # сработает при любом состоянии добавления новости
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Тест прерван", reply_markup=keyboards.ReplyKeyboardRemove())
    await message.answer(strings.GREETING, reply_markup=keyboards.start_keyboard())

@router.message(F.text.in_(["1️⃣", "2️⃣", "3️⃣"]), TestStates.question1)
async def question1(message: Message, state: FSMContext):
    data = await state.get_data()
    data[message.text] += 1
    await state.update_data(data)
    await message.answer("""<b>2. Какой характер кота вам ближе?</b>
 <b>1.</b> Спокойный и ласковый.
 <b>2.</b> Игривый и любопытный.
 <b>3.</b> Независимый и гордый.""", reply_markup=keyboards.test_reply_keyboard())
    await state.set_state(TestStates.question2)


@router.message(F.text.in_(["1️⃣", "2️⃣", "3️⃣"]), TestStates.question2)
async def question2(message: Message, state: FSMContext):
    data = await state.get_data()
    data[message.text] += 1
    await state.update_data(data)
    await message.answer("""<b>3. Сколько времени вы готовы уделять коту?</b>
 <b>1.</b> Много времени, готов(а) играть и ухаживать.
 <b>2.</b> Умеренно, но регулярно.
 <b>3.</b> Немного, но готов(а) обеспечить комфорт.""", reply_markup=keyboards.test_reply_keyboard())
    await state.set_state(TestStates.question3)

@router.message(F.text.in_(["1️⃣", "2️⃣", "3️⃣"]), TestStates.question3)
async def question3(message: Message, state: FSMContext):
    data = await state.get_data()
    data[message.text] += 1
    await state.update_data(data)
    await message.answer("""<b>4. Какой окрас кота вам нравится?</b>
 <b>1.</b> Серый, дымчатый, черный.
 <b>2.</b> Рыжий, полосатый, пятнистый.
 <b>3.</b> Белый, пушистый.""", reply_markup=keyboards.test_reply_keyboard())
    await state.set_state(TestStates.question4)

@router.message(F.text.in_(["1️⃣", "2️⃣", "3️⃣"]), TestStates.question4)
async def question4(message: Message, state: FSMContext):
    data = await state.get_data()
    data[message.text] += 1
    await state.update_data(data)
    await message.answer("""<b>5. Какой темперамент кота вам подходит?</b>
 <b>1.</b> Миролюбивый и послушный.
 <b>2.</b> Активный и любопытный.
 <b>3.</b> Независимый и неприступный.""", reply_markup=keyboards.test_reply_keyboard())
    await state.set_state(TestStates.question5)

@router.message(F.text.in_(["1️⃣", "2️⃣", "3️⃣"]), TestStates.question5)
async def question5(message: Message, state: FSMContext):
    data = await state.get_data()
    data[message.text] += 1
    await state.update_data(data)
    await message.answer("""<b>6. Есть ли у вас дети или другие животные?</b>
 <b>1.</b> Да, нужен кот, который ладит с другими.
 <b>2.</b> Нет, но хочу, чтобы кот был дружелюбным.
 <b>3.</b> Нет, предпочитаю кота, который не требует много внимания.""", reply_markup=keyboards.test_reply_keyboard())
    await state.set_state(TestStates.question6)

@router.message(F.text.in_(["1️⃣", "2️⃣", "3️⃣"]), TestStates.question6)
async def question6(message: Message, state: FSMContext):
    data = await state.get_data()
    data[message.text] += 1
    await state.update_data(data)
    await message.answer("""<b>7. Готовы ли вы ухаживать за котом, который нуждается в лечении?</b>
 <b>1.</b> Да, готов(а) помочь.
 <b>2.</b> Нет, предпочитаю здорового кота.
 <b>3.</b> Возможно, если это не требует больших усилий.""", reply_markup=keyboards.test_reply_keyboard())
    await state.set_state(TestStates.answer)

@router.message(TestStates.answer)
async def answer(message: Message, state: FSMContext):
    data = await state.get_data()
    
    name = best_match(results[max(data, key=data.get)])
    
    main_info = get_animal_info(name)
    
    await message.answer(await generate_animal_card_by_state(main_info, message))
    
    #await message.answer(f"вам подойдет котик {name}", reply_markup=keyboards.ReplyKeyboardRemove())
    #await message.answer(strings.GREETING, reply_markup=keyboards.start_keyboard())
    await state.clear()
    
@router.message(F.text, StatesGroupFilter(TestStates))
async def badInput(message: Message, state: FSMContext):
    await message.answer("Такого ответа нет", reply_markup=keyboards.test_reply_keyboard())
