from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def watch_animals_after_taking_keyboard():
    kb = [[KeyboardButton(text="Следующий котик")],
          [KeyboardButton(text="В меню")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard
