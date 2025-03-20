from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def all_questions_keyboard():
    kb = [[KeyboardButton(text="📗 Показать все вопросы")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard
