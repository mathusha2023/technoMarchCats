from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from states import TestStates, WatchAnimalsStates
import keyboards
from aiogram import Router, F, Bot
from utils.best_match import best_match
from utils.generate_animal_card_by_state import generate_animal_card_by_state
from utils.main_info import get_animal_info
import strings
from filters import StatesGroupFilter
from data import db_session
from data.users import User
from data.animals import Animal

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
    await message.answer("""<b>2. Какой характер кота Вам ближе?</b>
 <b>1️⃣</b> Спокойный и ласковый.
 <b>2️⃣</b> Игривый и любопытный.
 <b>3️⃣</b> Независимый и гордый.""", reply_markup=keyboards.test_reply_keyboard())
    await state.set_state(TestStates.question2)


@router.message(F.text.in_(["1️⃣", "2️⃣", "3️⃣"]), TestStates.question2)
async def question2(message: Message, state: FSMContext):
    data = await state.get_data()
    data[message.text] += 1
    await state.update_data(data)
    await message.answer("""<b>3. Сколько времени Вы готовы уделять коту?</b>
 <b>1️⃣</b> Много времени, готов(а) играть и ухаживать.
 <b>2️⃣</b> Умеренно, но регулярно.
 <b>3️⃣</b> Немного, но готов(а) обеспечить комфорт.""", reply_markup=keyboards.test_reply_keyboard())
    await state.set_state(TestStates.question3)

@router.message(F.text.in_(["1️⃣", "2️⃣", "3️⃣"]), TestStates.question3)
async def question3(message: Message, state: FSMContext):
    data = await state.get_data()
    data[message.text] += 1
    await state.update_data(data)
    await message.answer("""<b>4. Какой окрас кота Вам нравится?</b>
 <b>1️⃣</b> Серый, дымчатый, черный.
 <b>2️⃣</b> Рыжий, полосатый, пятнистый.
 <b>3️⃣</b> Белый, пушистый.""", reply_markup=keyboards.test_reply_keyboard())
    await state.set_state(TestStates.question4)

@router.message(F.text.in_(["1️⃣", "2️⃣", "3️⃣"]), TestStates.question4)
async def question4(message: Message, state: FSMContext):
    data = await state.get_data()
    data[message.text] += 1
    await state.update_data(data)
    await message.answer("""<b>5. Какой темперамент кота Вам подходит?</b>
 <b>1️⃣</b> Миролюбивый и послушный.
 <b>2️⃣</b> Активный и любопытный.
 <b>3️⃣</b> Независимый и неприступный.""", reply_markup=keyboards.test_reply_keyboard())
    await state.set_state(TestStates.question5)

@router.message(F.text.in_(["1️⃣", "2️⃣", "3️⃣"]), TestStates.question5)
async def question5(message: Message, state: FSMContext):
    data = await state.get_data()
    data[message.text] += 1
    await state.update_data(data)
    await message.answer("""<b>6. Есть ли у Вас дети или другие животные?</b>
 <b>1️⃣</b> Да, нужен кот, который ладит с другими.
 <b>2️⃣</b> Нет, но хочу, чтобы кот был дружелюбным.
 <b>3️⃣</b> Нет, предпочитаю кота, который не требует много внимания.""", reply_markup=keyboards.test_reply_keyboard())
    await state.set_state(TestStates.question6)

@router.message(F.text.in_(["1️⃣", "2️⃣", "3️⃣"]), TestStates.question6)
async def question6(message: Message, state: FSMContext):
    data = await state.get_data()
    data[message.text] += 1
    await state.update_data(data)
    await message.answer("""<b>7. Готовы ли Вы ухаживать за котом, который нуждается в лечении?</b>
 <b>1️⃣</b> Да, готов(а) помочь.
 <b>2️⃣</b> Нет, предпочитаю здорового кота.
 <b>3️⃣</b> Возможно, если это не требует больших усилий.""", reply_markup=keyboards.test_reply_keyboard())
    await state.set_state(TestStates.answer)

@router.message(TestStates.answer)
async def answer(message: Message, state: FSMContext):
    data = await state.get_data()
    
    id_ = best_match(results[max(data, key=data.get)])

    main_info = get_animal_info(id_)
    
    await generate_animal_card_by_state(main_info, message)
    await message.answer("можете оставить заявку", reply_markup=keyboards.final_test_keyboard())
    await state.set_state(TestStates.result)
    
@router.message(F.text == "в меню", TestStates.result, StatesGroupFilter(TestStates))
async def take(message: Message, state: FSMContext):
    if F.text == "📥 Хочу взять!":
        pass
    await message.answer(strings.GREETING, reply_markup=keyboards.start_keyboard())
    await state.clear()

@router.message(F.text == "📥 Хочу взять!", TestStates.result, StatesGroupFilter(TestStates))
async def take_cat(message: Message, state: FSMContext, bot: Bot):
    session = db_session.create_session()

    user = session.query(User).where(User.id == message.from_user.id).first()
    animal = session.query(Animal).where(
        Animal.id == user.lastWatchedAnimal).first()  # получаем последнее просмотренное пользователем животное
    if animal is None:  # последнее просмотренное пользователем животное имеет ID 0, то есть при последней попытке просмотра животное не было найдено
        return await message.answer("Сейчас Вы не можете взять животное!")

    last_request = session.query(AnimalRequest).where(and_(AnimalRequest.userId == user.id, AnimalRequest.animalId == animal.id)).first()  # ищем заявку от пользователя на это животное в базе данных
    if last_request:  # если такой запрос уже существует, то заново подавать запрос не будем
        return await message.answer("Заявка на этого котика ужа была подана и ожидает рассмотрения администратором. Пожалуйста, дождитесь обратной связи!")

    animal_request = AnimalRequest()
    animal_request.user = user
    animal_request.animal = animal
    session.add(animal_request)
    session.commit()

    await send_message_to_all_administrators(bot, "Подана новая заявка!")  # оповещаем всех администраторов о подаче заявки

    await state.update_data({"took": True})  # если котика только взяли ставим флаг

    await message.answer("Ваша заявка отправлена! Администратор свяжется с Вами в ближайшее время. Идём дальше?",
                         reply_markup=keyboards.watch_animals_after_taking_keyboard())

    
@router.message(F.text, StatesGroupFilter(TestStates))
async def badInput(message: Message, state: FSMContext):
    await message.answer("Такого ответа нет", reply_markup=keyboards.test_reply_keyboard())
