from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_volunteer_interaction_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Показать список волонтёров", callback_data="volunteer_list"))
    builder.row(InlineKeyboardButton(text="Обратиться к волонтерам", callback_data="volunteer_news"))
    builder.row(InlineKeyboardButton(text="Назад", callback_data="admin_menu"))
    return builder.as_markup()
