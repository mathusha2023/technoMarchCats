from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# from config import DONATE_LINK


def help_um_keyboard(is_volunteer):
    volunteer_text = "❌ Я больше не хочу быть волонтёром" if is_volunteer else "✅ Стать волонтёром"

    builder = InlineKeyboardBuilder()
    # builder.row(InlineKeyboardButton(text="Помочь копейкой", url=DONATE_LINK))
    builder.row(InlineKeyboardButton(text="💰 Поддержать нас копейкой", callback_data="fast_pay"),
                InlineKeyboardButton(text="📦 Помочь вещами", callback_data="partners_links_list"))
    builder.row(InlineKeyboardButton(text=volunteer_text, callback_data="volunteer"))
    builder.row(InlineKeyboardButton(text="◀️ Назад",
                                     callback_data="start"))
    return builder.as_markup()
