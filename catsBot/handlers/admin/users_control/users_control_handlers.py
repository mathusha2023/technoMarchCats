from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from data import db_session
from data.users import User
from middlewares import MediaGroupMiddleware
from states import UsersControlStates

from utils.generate_user_info_message import generate_user_info_message

router = Router()
router.message.middleware(MediaGroupMiddleware())


@router.message(F.text, UsersControlStates.searching_by_username)  # обработка поиска пользователя по юзернейму
async def search_user_by_username(message: Message, state: FSMContext):
    username = message.text.lstrip("@")
    session = db_session.create_session()
    user = session.query(User).where(User.username == username).first()
    if user is None:
        return await message.answer(f"Пользователь @{username} не найден! Проверьте введённые данные и попробуйте ещё раз")
    if user.id == message.from_user.id:
        return await message.answer("Это вы! Введите username другого пользователя")
    await generate_user_info_message(user, message)
    await state.update_data(user=user, session=session)

