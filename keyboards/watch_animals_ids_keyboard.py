from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def watch_animals_ids_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Показать список", callback_data="animals_admin_list"))
    builder.row(InlineKeyboardButton(text="<- Назад", callback_data="escape_to_admin_menu"))
    return builder.as_markup()
