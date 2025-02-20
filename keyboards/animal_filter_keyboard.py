from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def animal_filter_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Уменьшить мин. возраст", callback_data="min_age_down_filter"), InlineKeyboardButton(text="Увеличить мин. возраст", callback_data="min_age_up_filter"))
    builder.row(InlineKeyboardButton(text="Уменьшить макс. возраст", callback_data="max_age_down_filter"), InlineKeyboardButton(text="Увеличить макс. возраст", callback_data="max_age_up_filter"))
    builder.row(InlineKeyboardButton(text="Изменить пол питомца", callback_data="change_gender_filter"), InlineKeyboardButton(text="Изменить теги", callback_data="change_tags_filter"))
    return builder.as_markup()
