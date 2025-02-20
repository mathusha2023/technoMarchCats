from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
import keyboards
import strings
from data.animals_filters import AnimalFilter
from data.db_session import create_session
from data.users import User
from filters import StatesGroupFilter
from states import WatchAnimalsStates
from utils.generate_animal_filter_message import generate_animal_filter_message
from utils.generate_next_animal_card import generate_next_animal_card

router = Router()


@router.message(F.text == "В меню", StatesGroupFilter(WatchAnimalsStates))  # сработает при любом состоянии просмотра животных
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
async def next_cat(message: Message):
    await generate_next_animal_card(message.from_user.id, message)


@router.message(F.text == "Кошачий фильтр", WatchAnimalsStates.watching)
async def cats_filter(message: Message):
    session = create_session()
    animal_filter: AnimalFilter = session.query(User).where(User.id == message.from_user.id).first().filter
    await generate_animal_filter_message(message, animal_filter)
    