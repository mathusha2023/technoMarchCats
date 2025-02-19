from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
import strings
import keyboards
from states import AddAnimalStates

router = Router()


@router.callback_query(F.data == "animals")
async def contact_callback(callback: CallbackQuery):
    await callback.message.edit_text("Вот список возможных действий:", reply_markup=keyboards.admin_animals_keyboard())


@router.callback_query(F.data == "admin_menu")
async def back_callback(callback: CallbackQuery):
    await callback.message.edit_text(strings.ADMIN_MENU_CAPTION, reply_markup=keyboards.admin_menu_keyboard())


@router.callback_query(F.data == "add_animal")
async def add_animal_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddAnimalStates.naming)
    await callback.message.answer("Как зовут нашего нового котика?", reply_markup=keyboards.cancel_keyboard())
    await callback.answer()
