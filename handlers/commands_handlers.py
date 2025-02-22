from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
import config
from data import db_session
from data.animals_filters import AnimalFilter
from data.users import User
import strings
from filters import AdminFilter
import keyboards

router = Router()


@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    session = db_session.create_session()
    user_id = message.from_user.id
    if session.query(User).filter(
            User.id == user_id).first() is None:  # если в базе данных еще нет такого пользователя, то создаем его
        user = User()
        user.id = user_id
        user.username = message.from_user.username
        user.first_name = message.from_user.first_name
        if user_id == config.SUPERADMIN_ID:
            user.accessLevel = 3
        user_filter = AnimalFilter()
        user.filter = user_filter
        session.add(user_filter)
        session.add(user)
        session.commit()
    await state.clear()
    await message.answer(strings.GREETING, reply_markup=keyboards.start_keyboard())


@router.message(Command("help"))
async def help_(message: Message, state: FSMContext):
    s = "Вот список доступных команд:\n"
    for command in config.BOT_COMMANDS:
        s += f"/{command} - {config.BOT_COMMANDS[command]}\n"
    await state.clear()
    await message.answer(s, reply_markup=keyboards.ReplyKeyboardRemove())


@router.message(Command("about"))
async def about(message: Message):
    await message.answer(strings.INFO, reply_markup=keyboards.contacts_keyboard())


@router.message(Command("admin"), AdminFilter())
async def admin(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Добро пожаловать, админ!", reply_markup=keyboards.ReplyKeyboardRemove())
    await message.answer(strings.ADMIN_MENU_CAPTION, reply_markup=keyboards.admin_menu_keyboard())


@router.message(Command("admin"))
async def admin_denied(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Данная команда доступна только администраторам!",
                         reply_markup=keyboards.ReplyKeyboardRemove())
