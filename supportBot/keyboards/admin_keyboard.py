from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def admin_keyboard():
    kb = [[KeyboardButton(text="Отзывы&Пожелания")],
          [KeyboardButton(text="Добавить модератора"), KeyboardButton(text="Управление модераторами")],
          [KeyboardButton(text="Изменить приветствие"), KeyboardButton(text="Изменить вопросы по умолчанию")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard
