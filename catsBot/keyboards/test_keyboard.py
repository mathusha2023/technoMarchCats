from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def test_reply_keyboard():
    buttons = [
        [KeyboardButton(text="1️⃣"), KeyboardButton(text="2️⃣"), KeyboardButton(text="3️⃣")],
        [KeyboardButton(text="🚫 Отмена")]
    ]
    builder = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return builder
