from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def animal_filter_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⬇️ мин. возраст", callback_data="min_age_down_filter"), InlineKeyboardButton(text="⬆️ мин. возраст", callback_data="min_age_up_filter"))
    builder.row(InlineKeyboardButton(text="⬇️ макс. возраст", callback_data="max_age_down_filter"), InlineKeyboardButton(text="⬆️ макс. возраст", callback_data="max_age_up_filter"))
    builder.row(InlineKeyboardButton(text="📑 Изменить пол", callback_data="change_gender_filter"), InlineKeyboardButton(text="📑Изменить теги", callback_data="change_tags_filter"))
    return builder.as_markup()
