from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def back_keyboard():
        kb = [[KeyboardButton(text="Назад")]]
        keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        return keyboard
