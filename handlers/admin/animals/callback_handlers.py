from aiogram import Router, F
from aiogram.types import CallbackQuery
import strings
import keyboards

router = Router()


@router.callback_query(F.data == "animals")
async def contact_callback(callback: CallbackQuery):
    await callback.message.edit_text("Вот список возможных действий:", reply_markup=keyboards.admin_animals_keyboard())


@router.callback_query(F.data == "admin_menu")
async def back_callback(callback: CallbackQuery):
    await callback.message.edit_text(strings.ADMIN_MENU_CAPTION, reply_markup=keyboards.admin_menu_keyboard())
