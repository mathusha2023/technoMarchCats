from aiogram.types import Message
import keyboards
from data.users import User
from utils.get_text_access_level import get_text_access_level


# сообщение с информацией о пользователе для админа
async def generate_user_info_message(user: User, message: Message, edit=False):
    text = f"""Пользователь {user.firstName}:
tg: @{user.username}
роль: {get_text_access_level(user.accessLevel)}"""
    if user.isVolunteer:
        text += "\nВолонтёр"
    if user.isBanned:
        text += "\nЗаблокирован"
    is_admin = user.accessLevel > 1
    if edit:
        return await message.edit_text(text, reply_markup=keyboards.admin_user_control_keyboard(user.isBanned, is_admin))
    await message.answer(text, reply_markup=keyboards.admin_user_control_keyboard(user.isBanned, is_admin))

