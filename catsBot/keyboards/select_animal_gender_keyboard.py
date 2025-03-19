from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def select_animal_gender_keyboard():
        kb = [[KeyboardButton(text="1"), KeyboardButton(text="2")], [KeyboardButton(text="🚫 Отмена")]]
        keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        return keyboard
