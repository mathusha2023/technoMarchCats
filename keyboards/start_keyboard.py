from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🐈 Смотреть котов", callback_data="watch_animals"))
    builder.row(InlineKeyboardButton(text="📒 Подробнее о приюте", callback_data="start_about"),
                InlineKeyboardButton(text="📞 Связь с нами", callback_data="start_contact"))
    builder.row(InlineKeyboardButton(text="📥 Поддержать нас",
                                     url=f"https://vk.com/topic-88538029_31812031"))
    return builder.as_markup()
