from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def accept_adding_animal_keyboard():
        kb = [[KeyboardButton(text="✅ Да, все так"), KeyboardButton(text="✏️ Заполнить карточку заново")], [KeyboardButton(text="🚫 Отмена")]]
        keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        return keyboard
