from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def final_test_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="взять", callback_data='take'), InlineKeyboardButton(text="в меню", callback_data='menu'))
    return builder.as_markup()

