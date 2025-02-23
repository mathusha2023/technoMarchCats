from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from data import db_session
import keyboards
import strings
from sqlalchemy import and_
from data.animal_requests import AnimalRequest
from data.animals import Animal
from data.animals_filters import AnimalFilter
from data.db_session import create_session
from data.users import User
from filters import StatesGroupFilter
from states import WatchAnimalsStates
from utils.generate_animal_filter_message import generate_animal_filter_message
from utils.generate_next_animal_card import generate_next_animal_card
from utils.send_message_to_all_administrators import send_message_to_all_administrators

router = Router()


@router.message(F.text == "📂 В меню",
                StatesGroupFilter(WatchAnimalsStates))  # сработает при любом состоянии просмотра животных
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Надеюсь, вы нашли себе нового друга!", reply_markup=keyboards.ReplyKeyboardRemove())
    await message.answer(strings.GREETING, reply_markup=keyboards.start_keyboard())


@router.message(Command("cats"))
async def cats(message: Message, state: FSMContext):
    await state.set_state(WatchAnimalsStates.watching)
    await message.answer("Вот наши пушистые друзья. Может быть, вам кто-нибудь приглянется?",
                         reply_markup=keyboards.watch_animals_keyboard())
    await generate_next_animal_card(message.from_user.id, message)


@router.message(F.text == "↘️ Следующий котик", WatchAnimalsStates.watching)
async def next_cat(message: Message, state: FSMContext):
    data = await state.get_data()
    if data.get("took", False):  # если до этого котика только взяли, то надо поменять клавиатуру
        await message.answer("Продолжим просмотр пушистиков!", reply_markup=keyboards.watch_animals_keyboard())
        await state.set_data({"took": False})
    await generate_next_animal_card(message.from_user.id, message)


@router.message(F.text == "🔄 Кошачий фильтр", WatchAnimalsStates.watching)
async def cats_filter(message: Message):
    session = create_session()
    animal_filter: AnimalFilter = session.query(User).where(User.id == message.from_user.id).first().filter
    await generate_animal_filter_message(message, animal_filter)


@router.message(F.text == "📥 Хочу взять!", WatchAnimalsStates.watching)
async def take_cat(message: Message, state: FSMContext, bot: Bot):
    session = db_session.create_session()

    user = session.query(User).where(User.id == message.from_user.id).first()
    animal = session.query(Animal).where(
        Animal.id == user.lastWatchedAnimal).first()  # получаем последнее просмотренное пользователем животное
    if animal is None:  # последнее просмотренное пользователем животное имеет ID 0, то есть при последней попытке просмотра животное не было найдено
        return await message.answer("Сейчас вы не можете взять животное!")

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

    await message.answer("Ваша заявка отправлена! Администратор свяжется с вами в ближайшее время. Идём дальше?",
                         reply_markup=keyboards.watch_animals_after_taking_keyboard())
