from aiogram.filters import BaseFilter
from aiogram.types import Message
from data import db_session
from data.moderators import Moderator


class ModeratorFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        session = db_session.create_session()
        moders = session.query(Moderator).all()
        for m in moders:
            if m.user_id == message.from_user.id:
                return True
        return False
