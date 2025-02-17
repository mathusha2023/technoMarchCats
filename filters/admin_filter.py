from aiogram.filters import BaseFilter
from aiogram.types import Message
from data import db_session
from data.users import User


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        session = db_session.create_session()
        user = session.query(User).filter(User.id == message.from_user.id).first()
        return user.accessLevel > 1
