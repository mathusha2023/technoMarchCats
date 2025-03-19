from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def faq_keyboard():
    kb = [[KeyboardButton(text="📗 Часто задаваемые вопросы")], [KeyboardButton(text="📩 Задать вопрос")],
          [KeyboardButton(text="💡 Поделиться впечатлениями с нами")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard
