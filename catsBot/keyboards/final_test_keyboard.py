from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def final_test_keyboard():
    buttons = [
        [KeyboardButton(text="📥 Хочу взять!")],
        [KeyboardButton(text="📂 В меню")]
    ]
    builder = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return builder