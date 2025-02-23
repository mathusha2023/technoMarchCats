from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def delete_request_keyboard(request_id):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="❌ Закрыть заявку", callback_data=f"delete_request_{request_id}"))
    return builder.as_markup()
