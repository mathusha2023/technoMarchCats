from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def change_default_questions_keyboard():
    kb = [[KeyboardButton(text="Изменить ответы")], [KeyboardButton(text="Добавить вопрос/ответ")],
          [KeyboardButton(text="Удалить вопрос")], [KeyboardButton(text="Отмена")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard
