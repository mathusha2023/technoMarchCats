from aiogram import Router, F
from aiogram.types import CallbackQuery

import config
import strings
import keyboards
from filters import BannedFilter
from data.db_session import create_session
from data.users import User

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


@router.callback_query(F.data == "help_um")
async def help_um_callback(callback: CallbackQuery):
    session = create_session()
    user = session.query(User).where(User.id == callback.from_user.id).first()

    await callback.message.edit_text(strings.HELP, reply_markup=keyboards.help_um_keyboard(user.isVolunteer))


@router.callback_query(F.data == "partners_list")
async def partners_list_callback(callback: CallbackQuery):
    text = "Вот список магазинов-партнеров:\n\n"

    for p in config.PARTNERS:
        text += f"🔹 {p}\n"

    await callback.message.edit_text(text, reply_markup=keyboards.to_help_um_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data == "start")
async def start_callback(callback: CallbackQuery):
    await callback.message.edit_text(strings.GREETING, reply_markup=keyboards.start_keyboard())
