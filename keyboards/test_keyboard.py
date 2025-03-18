from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def test_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="А", callback_data="А"))
    builder.row(InlineKeyboardButton(text="Б", callback_data="Б"))
    builder.row(InlineKeyboardButton(text="В", callback_data="В"))
    return builder.as_markup()
