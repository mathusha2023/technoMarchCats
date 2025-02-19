from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def watch_animals_keyboard():
        kb = [[KeyboardButton(text="Хочу взять!"), KeyboardButton(text="Следующий")], [KeyboardButton(text="В меню")]]
        keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        return keyboard
