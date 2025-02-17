from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_animals_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Добавить животное", callback_data="add_animal"),
                InlineKeyboardButton(text="Удалить животное", callback_data="delete_animal"))
    builder.row(InlineKeyboardButton(text="Редактировать информацию животного", callback_data="update_animal"))
    builder.row(InlineKeyboardButton(text="<- Назад", callback_data="admin_menu"))
    return builder.as_markup()
