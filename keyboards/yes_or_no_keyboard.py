from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def yes_or_no_keyboard():
        kb = [[KeyboardButton(text="Да"), KeyboardButton(text="Нет")], [KeyboardButton(text="Отмена")]]
        keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        return keyboard
