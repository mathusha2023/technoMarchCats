from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_user_control_keyboard(is_banned=False, is_admin=False):
    builder = InlineKeyboardBuilder()
    ban_text = "Разблокировать" if is_banned else "Заблокировать"
    builder.row(InlineKeyboardButton(text=ban_text, callback_data="ban_user"))
    if not is_admin:
        builder.row(InlineKeyboardButton(text="👨‍💻 Назначить администратором", callback_data="make_admin"))
    builder.row(InlineKeyboardButton(text="🚫 Отмена", callback_data="cancel_user_controlling"))
    return builder.as_markup()
