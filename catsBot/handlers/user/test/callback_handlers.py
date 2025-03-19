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
        "А": ["Спокойный", "Ласковый", "Послушный", "Домашний", "Серый", "Дымчатый"],
        "Б": ["Игривый", "Активный", "Любопытный", "Рыжий", "Полосатый", "Пушистый"],
        "В": ["Гордый", "Неприступный", "Непривередливый", "Черный", "Белый", "Пятнистый"]
    }

@router.message(F.text == "🚫 Отмена",
                StatesGroupFilter(TestStates))  # сработает при любом состоянии добавления новости
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Тест прерван", reply_markup=keyboards.ReplyKeyboardRemove())
    await message.answer(strings.GREETING, reply_markup=keyboards.start_keyboard())

@router.message(F.text.in_(["А", "Б", "В"]), TestStates.question1)
async def question1(message: Message, state: FSMContext):
    data = await state.get_data()
    data[message.text] += 1
    await state.update_data(data)
    await message.answer("""<br>2. Какой характер кота вам ближе?</br>
 <br>А)</br> Спокойный и ласковый.
 <br>Б)</br> Игривый и любопытный.
 <br>В)</br> Независимый и гордый.""", reply_markup=keyboards.test_reply_keyboard())
    await state.set_state(TestStates.question2)


@router.message(F.text.in_(["А", "Б", "В"]), TestStates.question2)
async def question2(message: Message, state: FSMContext):
    data = await state.get_data()
    data[message.text] += 1
    await state.update_data(data)
    await message.answer("""<br>3. Сколько времени вы готовы уделять коту?</br>
 <br>А)</br> Много времени, готов(а) играть и ухаживать.
 <br>Б)</br> Умеренно, но регулярно.
 <br>В)</br> Немного, но готов(а) обеспечить комфорт.""", reply_markup=keyboards.test_reply_keyboard())
    await state.set_state(TestStates.question3)

@router.message(F.text.in_(["А", "Б", "В"]), TestStates.question3)
async def question3(message: Message, state: FSMContext):
    data = await state.get_data()
    data[message.text] += 1
    await state.update_data(data)
    await message.answer("""<br>4. Какой окрас кота вам нравится?</br>
 <br>А)</br> Серый, дымчатый, черный.
 <br>Б)</br> Рыжий, полосатый, пятнистый.
 <br>В)</br> Белый, пушистый.""", reply_markup=keyboards.test_reply_keyboard())
    await state.set_state(TestStates.question4)

@router.message(F.text.in_(["А", "Б", "В"]), TestStates.question4)
async def question4(message: Message, state: FSMContext):
    data = await state.get_data()
    data[message.text] += 1
    await state.update_data(data)
    await message.answer("""<br>5. Какой темперамент кота вам подходит?</br>
 <br>А)</br> Миролюбивый и послушный.
 <br>Б)</br> Активный и любопытный.
 <br>В)</br> Независимый и неприступный.""", reply_markup=keyboards.test_reply_keyboard())
    await state.set_state(TestStates.question5)

@router.message(F.text.in_(["А", "Б", "В"]), TestStates.question5)
async def question5(message: Message, state: FSMContext):
    data = await state.get_data()
    data[message.text] += 1
    await state.update_data(data)
    await message.answer("""<br>6. Есть ли у вас дети или другие животные?</br>
 <br>А)</br> Да, нужен кот, который ладит с другими.
 <br>Б)</br> Нет, но хочу, чтобы кот был дружелюбным.
 <br>В)</br> Нет, предпочитаю кота, который не требует много внимания.""", reply_markup=keyboards.test_reply_keyboard())
    await state.set_state(TestStates.question6)

@router.message(F.text.in_(["А", "Б", "В"]), TestStates.question6)
async def question6(message: Message, state: FSMContext):
    data = await state.get_data()
    data[message.text] += 1
    await state.update_data(data)
    await message.answer("""<br>7. Готовы ли вы ухаживать за котом, который нуждается в лечении?</br>
 <br>А)</br> Да, готов(а) помочь.
 <br>Б)</br> Нет, предпочитаю здорового кота.
 <br>В)</br> Возможно, если это не требует больших усилий.""", reply_markup=keyboards.test_reply_keyboard())
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
