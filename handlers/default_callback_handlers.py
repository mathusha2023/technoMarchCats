from aiogram import Router, F
from aiogram.types import CallbackQuery
import strings
import keyboards
from filters import BannedFilter

router = Router()


@router.message(BannedFilter())
async def answer_for_banned(callback: CallbackQuery):
    await callback.message.answer(strings.BANNED_USERS_MESSAGE, reply_markup=keyboards.ReplyKeyboardRemove())


@router.callback_query(F.data == "contact")
async def contact_callback(callback: CallbackQuery):
    await callback.message.edit_text(strings.CONTACTS, reply_markup=keyboards.about_keyboard())


@router.callback_query(F.data == "about")
async def about_callback(callback: CallbackQuery):
    await callback.message.edit_text(strings.INFO, reply_markup=keyboards.contacts_keyboard())


@router.callback_query(F.data == "start_contact")
async def start_contact_callback(callback: CallbackQuery):
    await callback.message.edit_text(strings.CONTACTS, reply_markup=keyboards.to_start_menu_keyboard())


@router.callback_query(F.data == "start_about")
async def start_about_callback(callback: CallbackQuery):
    await callback.message.edit_text(strings.INFO, reply_markup=keyboards.to_start_menu_keyboard())


@router.callback_query(F.data == "start")
async def start_callback(callback: CallbackQuery):
    await callback.message.edit_text(strings.GREETING, reply_markup=keyboards.start_keyboard())
