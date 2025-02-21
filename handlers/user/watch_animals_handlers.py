from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from data import db_session
import keyboards
import strings
from data.animal_requests import AnimalRequest
from data.animals import Animal
from data.animals_filters import AnimalFilter
from data.db_session import create_session
from data.users import User
from filters import StatesGroupFilter
from states import WatchAnimalsStates
from utils.generate_animal_filter_message import generate_animal_filter_message
from utils.generate_next_animal_card import generate_next_animal_card

router = Router()


@router.message(F.text == "В меню",
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


@router.message(F.text == "Следующий котик", WatchAnimalsStates.watching)
async def next_cat(message: Message, state: FSMContext):
    data = await state.get_data()
    if data.get("took", False):  # если до этого котика только взяли, то надо поменять клавиатуру
        await message.answer("Продолжим просмотр пушистиков!", reply_markup=keyboards.watch_animals_keyboard())
        await state.set_data({"took": False})
    await generate_next_animal_card(message.from_user.id, message)


@router.message(F.text == "Кошачий фильтр", WatchAnimalsStates.watching)
async def cats_filter(message: Message):
    session = create_session()
    animal_filter: AnimalFilter = session.query(User).where(User.id == message.from_user.id).first().filter
    await generate_animal_filter_message(message, animal_filter)


@router.message(F.text == "Хочу взять!", WatchAnimalsStates.watching)
async def take_cat(message: Message, state: FSMContext):
    session = db_session.create_session()

    animal_request = AnimalRequest()
    user = session.query(User).where(User.id == message.from_user.id).first()
    animal = session.query(Animal).where(
        Animal.id == user.lastWatchedAnimal).first()  # получаем последнее просмотренное пользователем животное
    animal_request.user = user
    animal_request.animal = animal
    session.add(animal_request)
    session.commit()

    await state.update_data({"took": True})  # если котика только взяли ставим флаг

    await message.answer("Ваша заявка отправлена! Администратор свяжется с вами в ближайшее время. Идём дальше?",
                         reply_markup=keyboards.watch_animals_after_taking_keyboard())
