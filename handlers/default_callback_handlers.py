from aiogram import Router, F
from aiogram.types import CallbackQuery
import strings
from keyboards import contacts_keyboard, about_keyboard

router = Router()


@router.callback_query(F.data == "contact")
async def contact_callback(callback: CallbackQuery):
    await callback.message.edit_text(strings.CONTACTS, reply_markup=about_keyboard())


@router.callback_query(F.data == "about")
async def back_callback(callback: CallbackQuery):
    await callback.message.edit_text(strings.INFO, reply_markup=contacts_keyboard())
