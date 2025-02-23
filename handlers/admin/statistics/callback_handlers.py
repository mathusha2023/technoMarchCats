from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from states import AddNewsStates
import keyboards
from aiogram import Router, F, Bot
from data.db_session import create_session
from data.users import User
from data.animal_requests import AnimalRequest
from keyboards import hide_message_keyboard

router = Router()

@router.callback_query(F.data == "hide_stats")
async def delete_request_callback(callback: CallbackQuery, bot: Bot):
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await callback.answer()

@router.callback_query(F.data == "stats")
async def stats_callback(callback: CallbackQuery, state: FSMContext, bot: Bot):
    with create_session() as session: # подсчет пользователей
        all_users = session.query(User).all() 
        requests_count = session.query(AnimalRequest).count()
        
    user_count = 0
    admin_count = 0
    banned_count = 0
    for user in all_users:
        user_count += user.accessLevel < 2
        admin_count += user.accessLevel > 1
        # TODO banned count
    
    donations_count = 0 # TODO donations count

    text = f"📊 Наша статистика:\n🔹 обычных пользователей: {user_count}\n🔹 администраторов: {admin_count}\n🔹 забаненных: {banned_count}\n➖➖➖➖➖➖➖➖➖➖\n🔹 заявок: {requests_count}\n➖➖➖➖➖➖➖➖➖➖\n🔹 пожертвований: {donations_count}\n"
    if len(text) > 4096:
        text = text[:4096]
    
    await bot.send_message(chat_id=callback.message.chat.id, text=text, reply_markup=hide_message_keyboard())
    await callback.answer()
