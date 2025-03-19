from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def close_animals_admin_list_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="❌ Закрыть", callback_data="close_animals_admin_list"))
    return builder.as_markup()
