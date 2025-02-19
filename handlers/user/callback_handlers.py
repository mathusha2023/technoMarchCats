from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
import keyboards
from states import WatchAnimalsStates
from utils.generate_next_animal_card import generate_next_animal_card

router = Router()


@router.callback_query(F.data == "watch_animals")
async def cats_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(WatchAnimalsStates.watching)
    await callback.message.answer("Вот наши пушистые друзья. Может быть, вам кто-нибудь приглянется?",
                         reply_markup=keyboards.watch_animals_keyboard())
    await generate_next_animal_card(callback.from_user.id, callback.message)
    await callback.answer()
