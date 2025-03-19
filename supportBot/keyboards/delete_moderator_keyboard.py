from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def delete_moderator_keyboard():
    kb = [[KeyboardButton(text="❌ Удалить модератора")], [KeyboardButton(text="Отменить приглашение модератора")],
          [KeyboardButton(text="🚫 Отмена")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard
