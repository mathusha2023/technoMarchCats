from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def test_reply_keyboard():
    buttons = [
        [KeyboardButton(text="А"), KeyboardButton(text="Б"), KeyboardButton(text="В")],
        [KeyboardButton(text="🚫 Отмена")]
    ]
    builder = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return builder
