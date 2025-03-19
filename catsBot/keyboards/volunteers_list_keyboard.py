from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def volunteers_list_keyboard(users, fourth_number, show_left=False, show_right=False):
    builder = InlineKeyboardBuilder()

    row = []
    for i in range(len(users)):
        user = users[i]
        row.append(InlineKeyboardButton(text=f"{user.firstName}\n@{user.username}", callback_data=f"volunteer_control_{user.id}"))
        if (i + 1) % 2 == 0 or i == len(users) - 1:
            builder.row(*row)
            row.clear()


    row = [InlineKeyboardButton(text="◀️ Назад", callback_data="volunteers_interaction")]
    if show_left:
        row.insert(0, InlineKeyboardButton(text="◀️",
                                           callback_data=f"volunteer_control_left_{fourth_number}"))  # номер четверки тегов
    if show_right:
        row.insert(2, InlineKeyboardButton(text="▶️",
                                           callback_data=f"volunteer_control_right_{fourth_number}"))  # номер четверки тегов

    builder.row(*row)
    return builder.as_markup()
