from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🐾 Животные", callback_data="animals"),
                InlineKeyboardButton(text="📑 Заявки на опекунство", callback_data="guardianship_list"))
    builder.row(InlineKeyboardButton(text="🌐 Опубликовать новость", callback_data="post_news"),
                InlineKeyboardButton(text="📊 Статистика", callback_data="stats"))
    builder.row(InlineKeyboardButton(text="🛗 Управление пользователями", callback_data="users_control"))
    builder.row(InlineKeyboardButton(text="Обратиться к волонтерам", callback_data="volunteer_news"))
    return builder.as_markup()
