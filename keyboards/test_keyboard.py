from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def test_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="А", callback_data="А"))
    builder.row(InlineKeyboardButton(text="Б", callback_data="Б"))
    builder.row(InlineKeyboardButton(text="В", callback_data="В"))
    return builder.as_markup()

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def test_reply_keyboard():
    buttons = [
        [KeyboardButton(text="А")],
        [KeyboardButton(text="Б")],
        [KeyboardButton(text="В")],
        [KeyboardButton(text="🚫 Отмена")]
    ]
    builder = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return builder

