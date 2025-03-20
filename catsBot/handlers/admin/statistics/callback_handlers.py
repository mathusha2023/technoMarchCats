from aiogram.types import CallbackQuery
from aiogram import Router, F

from config import BANNED_USERS
from data.db_session import create_session
from data.statistics import Statistic
from data.users import User
from data.animal_requests import AnimalRequest
from handlers.user.callback_handlers import volunteer_callback
from keyboards import hide_message_keyboard

router = Router()


@router.callback_query(F.data == "hide_stats")
async def hide_stats_callback(callback: CallbackQuery):
    await callback.message.delete()


@router.callback_query(F.data == "stats")
async def stats_callback(callback: CallbackQuery):
    with create_session() as session:  # подсчет пользователей
        all_users = session.query(User).all()
        requests_count = session.query(AnimalRequest).count()
        statistic = session.query(Statistic).first()
        donates_count = statistic.donatesCount
        donates_sum = statistic.donatesSum

    all_count = 0
    user_count = 0
    admin_count = 0
    volunteer_count = 0
    for user in all_users:
        all_count += 1
        user_count += user.accessLevel < 2
        admin_count += user.accessLevel > 1
        volunteer_count += user.isVolunteer

    banned_count = len(BANNED_USERS)


    text = f"📊 Наша статистика:\n🔹 всего пользователей: {all_count}\n🔹 обычных пользователей: {user_count}\n🔹 администраторов: {admin_count}\n🔹 волонтёров: {volunteer_count}\n🔹 заблокированных пользователей: {banned_count}\n➖➖➖➖➖➖➖➖➖➖\n🔹 заявок: {requests_count}\n🔹 число пожертвований: {donates_count}\n🔹 сумма пожертвований: {donates_sum} RUB"
    if len(text) > 4096:
        text = text[:4096]

    await callback.message.answer(text, reply_markup=hide_message_keyboard())
    await callback.answer()
