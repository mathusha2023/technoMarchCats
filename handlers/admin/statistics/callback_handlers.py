from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from states import AddNewsStates
import keyboards
from aiogram import Router, F, Bot
from data.db_session import create_session
from data.users import User
from data.animal_requests import AnimalRequest

router = Router()

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

    text = f"обычных пользователей: {user_count}\nадминов: {admin_count}\nзабаненных: {banned_count}\n//////////////////////////\nзаявок: {requests_count}\n//////////////////////////\nпожертвований: {donations_count}\n"
    if len(text) > 4096:
        text = text[:4096]
    
    await bot.send_message(chat_id=callback.message.chat.id, text=text)
    await callback.answer()

