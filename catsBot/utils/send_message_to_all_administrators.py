from aiogram import Bot
from data.db_session import create_session
from data.users import User


# отправка сообщения всем администраторам
async def send_message_to_all_administrators(bot: Bot, text):
    session = create_session()
    administrators = session.query(User).where(User.accessLevel > 1).all()

    for admin in administrators:
        await bot.send_message(admin.id, text)
