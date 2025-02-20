from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def animal_tags_filter_keyboard(tags, fourth_number, show_left=False, show_right=False):
    builder = InlineKeyboardBuilder()

    row = []
    for i in range(len(tags)):
        row.append(InlineKeyboardButton(text=tags[i], callback_data=f"tags_filter_{tags[i]}"))
        if (i + 1) % 2 == 0 or i == len(tags) - 1:
            builder.row(*row)
            row.clear()

    row = [InlineKeyboardButton(text="Назад", callback_data="back_filter")]
    if show_left:
        row.insert(0, InlineKeyboardButton(text="<-",
                                           callback_data=f"tags_filter_left_{fourth_number}"))  # номер четверки тегов
    if show_right:
        row.insert(2, InlineKeyboardButton(text="->",
                                           callback_data=f"tags_filter_right_{fourth_number}"))  # номер четверки тегов

    builder.row(*row)
    return builder.as_markup()
