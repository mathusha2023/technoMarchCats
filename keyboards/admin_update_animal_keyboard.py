from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def admin_update_animal_keyboard():
    kb = [[KeyboardButton(text="🐈‍⬛ Имя"), KeyboardButton(text="❓ Пол"), KeyboardButton(text="📅 Дату рождения")],
          [KeyboardButton(text="📑 Описание"), KeyboardButton(text="🖼️ Фотографии"), KeyboardButton(text="🗒️ Теги")],
          [KeyboardButton(text="📂 В меню"), KeyboardButton(text="✅ Сохранить")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard
