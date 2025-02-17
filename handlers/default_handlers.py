from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from data import db_session
from data.users import User

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    session = db_session.create_session()
    user_id = message.from_user.id
    if session.query(User).filter(User.id == user_id).first() is None:
        user = User()
        user.id = user_id
        user.username = message.from_user.first_name
        session.add(user)
        session.commit()

    await message.answer("Hello!")
