from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def hide_message_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="скрыть", callback_data="hide_stats"))
    return builder.as_markup()