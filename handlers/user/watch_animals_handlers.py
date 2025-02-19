from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
import keyboards
import strings
from filters import StatesGroupFilter
from states import WatchAnimalsStates
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


@router.message(F.text == "Следующий", WatchAnimalsStates.watching)
async def next_cat(message: Message):
    await generate_next_animal_card(message.from_user.id, message)
