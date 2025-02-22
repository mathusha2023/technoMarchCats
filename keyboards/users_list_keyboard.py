from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def users_list_keyboard(users, fourth_number, show_left=False, show_right=False):
    builder = InlineKeyboardBuilder()

    row = []
    for i in range(len(users)):
        user = users[i]
        row.append(InlineKeyboardButton(text=f"{user.firstName}\n@{user.username}", callback_data=f"user_control_{user.id}"))
        if (i + 1) % 2 == 0 or i == len(users) - 1:
            builder.row(*row)
            row.clear()

    builder.row(InlineKeyboardButton(text="Поиск пользователя по telegram username", callback_data="search_user_by_username"))

    row = [InlineKeyboardButton(text="Назад", callback_data="admin_menu")]
    if show_left:
        row.insert(0, InlineKeyboardButton(text="<-",
                                           callback_data=f"user_control_left_{fourth_number}"))  # номер четверки тегов
    if show_right:
        row.insert(2, InlineKeyboardButton(text="->",
                                           callback_data=f"user_control_right_{fourth_number}"))  # номер четверки тегов

    builder.row(*row)
    return builder.as_markup()
