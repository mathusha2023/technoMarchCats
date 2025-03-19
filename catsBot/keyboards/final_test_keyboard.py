from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def final_test_keyboard():
    buttons = [
        [KeyboardButton(text="взять"),
        KeyboardButton(text="в меню")]
    ]
    builder = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return builder