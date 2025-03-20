from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def moderator_answer_keyboard(question_id: int):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="📨  Ответить!", callback_data=str(question_id)))
    return builder.as_markup()
