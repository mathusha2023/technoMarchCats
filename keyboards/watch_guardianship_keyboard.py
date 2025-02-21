from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def watch_guardianship_keyboard():
    kb = [[KeyboardButton(text="В меню"), KeyboardButton(text="Следующая")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard
