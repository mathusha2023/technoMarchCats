from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
import logging

from config import BANNED_USERS
from data import db_session
import strings
import keyboards
from data.users import User
from states import UsersControlStates
from utils.generate_user_info_message import generate_user_info_message
import config

router = Router()


@router.callback_query(F.data == "users_control")  # отображаем первую страницу списка пользователей
async def watch_users_callback(callback: CallbackQuery):
    session = db_session.create_session()
    users = session.query(User).limit(4).all()
    users_count = session.query(User).count()

    await callback.message.edit_text(strings.USERS_CONTROL_CAPTION,
                                     reply_markup=keyboards.users_list_keyboard(users, 1, show_right=users_count > 4))


@router.callback_query(F.data.startswith("user_control_right_"))  # перелистывание списка пользователей вправо по кнопке
async def user_control_right_callback(callback: CallbackQuery):
    fourth_number = int(
        callback.data.split("_")[-1])  # получаем номер последней четверки, в которой находился пользователь
    session = db_session.create_session()
    users = session.query(User).offset(fourth_number * 4).limit(4).all()
    users_count = session.query(User).count()
    await callback.message.edit_reply_markup(
        reply_markup=keyboards.users_list_keyboard(users, fourth_number + 1, show_left=True,
                                                   show_right=users_count > (fourth_number + 1) * 4))
    await callback.answer()


@router.callback_query(F.data.startswith("user_control_left_"))  # перелистывание списка пользователей влево по кнопке
async def user_control_left_callback(callback: CallbackQuery):
    fourth_number = int(
        callback.data.split("_")[-1])  # получаем номер последней четверки, в которой находился пользователь
    session = db_session.create_session()
    users = session.query(User).offset((fourth_number - 2 if fourth_number > 1 else 0) * 4).limit(4).all()
    await callback.message.edit_reply_markup(
        reply_markup=keyboards.users_list_keyboard(users, fourth_number - 1, show_right=True,
                                                   show_left=fourth_number > 2))
    await callback.answer()


@router.callback_query(F.data.startswith("search_user_by_username"))  # переход в режим поиска по юзернейму
async def search_user_by_username_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UsersControlStates.searching_by_username)
    await callback.message.edit_text("Пришлите telegram username пользователя, которого хотите найти",
                                     reply_markup=keyboards.cancel_user_searching_keyboard())
    await callback.answer()


@router.callback_query(F.data.startswith("cancel_user_searching"))
async def cancel_user_searching_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await watch_users_callback(callback)  # переходим обратно к просмотру пользователей


@router.callback_query(F.data.startswith("user_control_"))  # выбор администратором пользователя совершен
async def user_control(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.data.split("_")[-1])  # получаем telegram user_id выбранного пользователя
    session = db_session.create_session()
    user = session.query(User).where(User.id == user_id).first()
    if user.id == callback.from_user.id:
        return await callback.answer("Это вы!")
    await generate_user_info_message(user, callback.message)
    await state.update_data(user=user, session=session)
    await callback.answer()


@router.callback_query(F.data.startswith("ban_user"))
async def ban_user_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        session = data["session"]
        user = data["user"]
    except KeyError:
        logging.debug("В контексте нет полей session и user")
        return await callback.answer("Ошибка! Попробуйте заново выбрать пользователя")
    if user.accessLevel > 1 and callback.from_user.id != config.SUPERADMIN_ID:
        return await callback.answer("Вы не можете заблокировать администратора")
    if user.isBanned:
        BANNED_USERS.remove(user.id)  # если пользователь был заблокирован, то убирает его из списка забаненных
    else:
        BANNED_USERS.append(user.id)
    user.isBanned = not user.isBanned
    session.commit()
    await generate_user_info_message(user, callback.message, edit=True)


@router.callback_query(F.data.startswith("make_admin"))
async def make_admin_callback(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    try:
        session = data["session"]
        user = data["user"]
    except KeyError:
        logging.debug("В контексте нет полей session и user")
        return await callback.answer("Ошибка! Попробуйте заново выбрать пользователя")
    if user.accessLevel < 2:
        user.accessLevel = 2
        session.commit()
        try:
            await bot.send_message(user.id, "Вы были назначены администратором бота!")
        except TelegramBadRequest:
            logging.info(f"Пользователя {user.id} не существует!")
        return await generate_user_info_message(user, callback.message, edit=True)
    await callback.answer()


@router.callback_query(F.data.startswith("cancel_user_controlling"))
async def cancel_user_controlling_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
